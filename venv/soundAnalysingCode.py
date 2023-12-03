import python3_midi as p3m
import matplotlib.pyplot as plt
import os
from scipy.io import wavfile
import numpy as np

def ChooseSoundToPlay():
    print("Choose the number of the file you'd like to load:")
    assets = os.listdir('assets/Wav Notes')
    num = 0
    itemsInAssets = []
    for compos in assets:
        num = num + 1
        composNum = str(num)
        itemsInAssets.append(compos)
        print(composNum + " - " + compos + "\n")

    whichAsset = input()
    whichAsset = int(whichAsset)
    name = 'assets/Wav Notes/' + itemsInAssets[whichAsset - 1]
    return name

def PlotSound(path):
    # Replace 'your_audio_file.wav' with the path to your WAV file
    sample_rate, audio_data = wavfile.read(path)

    # If stereo, select only one channel (e.g., left channel)
    # audio_data = audio_data[:, 0]  # Uncomment this line if needed

    # Normalize to range [-1, 1]
    audio_data_normalized = abs(audio_data[:,1] / np.max(abs(audio_data[:,1])))

    # Create a time axis for the waveform
    time = [i / sample_rate for i in range(len(audio_data_normalized))]

    # Plot the waveform
    plt.plot(time, audio_data_normalized)
    plt.show()

    fft_result = np.fft.fft(audio_data_normalized)
    frequency_bins = np.fft.fftfreq(len(fft_result))
    plt.plot(frequency_bins, np.abs(fft_result))
    plt.show()

def GetHarmoniesForDataBase(path):

    # First, we read the audio from the wav:
    samplingRate , audio = wavfile.read(path)

    # Then, we normalize and remove the DC offset:
    audio = abs(audio[:, 1] / np.max(abs(audio[:, 1])))
    audio -= np.mean(audio)

    # We FFT it:
    audio = np.fft.fft(audio)
    bins = np.fft.fftfreq(len(audio))

    # Then we finally get the frequencies in which there are spikes:
    spikes = [x for x in range(0, len(audio)) if audio[x] > 0.3 * np.max(audio) and bins[x] > 0.002]
    spikesFreqs = []
    for x in range(0,len(spikes)):
        if x > 0 and bins[spikes[x]] - bins[spikes[x-1]] > 0.001:
            spikesFreqs.append(bins[spikes[x-1]])
    spikesFreqs.append(bins[spikes[len(spikes) - 1]])
    return spikesFreqs

def GetHarmoniesOfInput(audio):

    # We preprocess the audio input:
    audio = np.array(audio[0])
    audio = abs(audio[:, 1] / np.max(abs(audio[:, 1])))
    audio -= np.mean(audio)

    # We FFT it:
    audio = np.fft.fft(abs(audio))
    bins = np.fft.fftfreq(len(audio))

    # Then we finally get the frequencies in which there are spikes:
    spikes = [x for x in range(0, len(audio)) if audio[x] > 0.05 * max(audio) and bins[x] > 0.002]
    spikesFreqs = []
    for x in range(0, len(spikes)):
        if x > 0 and bins[spikes[x]] - bins[spikes[x - 1]] > 0.001:
            spikesFreqs.append(bins[spikes[x - 1]])
    spikesFreqs.append(bins[spikes[len(spikes) - 1]])
    return spikesFreqs

def CompareHarmonies(dic, input):

    # If the input has way more harmonies than the harmonies in any of the keys, then this must mean that it wasn't a key that was played:
    temp = False
    for _, note in dic.items():
        if not len(note) <= 0.7 * len(input):
            temp = True
    if not temp:
        return temp

    for _, note in dic.items():
        # We check how many harmonies of the note G match with the harmonies of the input:
        matches = [x for x in input for y in note if y - 0.002 <= x <= y + 0.002]
        # And if the number of matches isn't too small then we can assume that it was a key that was played:
        if not len(matches) <= 0.7 * len(input):
            return True

    # If all checks are failed, then we can assume that a note wasn't played:
    return False