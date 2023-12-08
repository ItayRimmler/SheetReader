import python3_midi as p3m
import matplotlib.pyplot as plt
import os
from scipy.io import wavfile
import numpy as np
import pickle


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
    #sample_rate, audio_data = wavfile.read(path)
    audio_data = np.array(path[0])

    # If stereo, select only one channel (e.g., left channel)
    # audio_data = audio_data[:, 0]  # Uncomment this line if needed

    # Normalize to range [-1, 1]
    audio_data_normalized = abs(audio_data[:,1] / np.max(abs(audio_data[:,1])))

    # Create a time axis for the waveform
    #time = [i / sample_rate for i in range(len(audio_data_normalized))]

    # Plot the waveform
    #plt.plot(time, audio_data_normalized)
    #plt.show()

    fft_result = np.fft.fft(audio_data_normalized)
    frequency_bins = np.fft.fftfreq(len(fft_result))
    plt.plot(frequency_bins, np.abs(fft_result))
    plt.show()

def SaveHarmoniesForDataBase(HarmoniesDictionary = None):
    # Choose whether to add to an existing dictionary:
    if HarmoniesDictionary == None:
        HarmoniesDictionary = {}


    # Choose the name of the key:
    key = input("Choose the name of the key you want to record (capital letters only):\n")

    # Choose how many harmonies to record
    numOfHarmonies = input("Choose how many harmonies to record (default is 5):\n")
    if not type(numOfHarmonies) == int or numOfHarmonies < 1:
        numOfHarmonies = 5

    # Let's import to avoid of circular importing:
    from soundDetectionCode import DetectAnySound

    # Setting yeses to 0:
    yeses = 0

    # Choosing whether to get a wav file's sound:
    answer1 = input("Would you like to add the first sound from an existing wav file in ./assets? [Y/N]\n")
    if answer1 == 'Y' or answer1 == 'y':
        HarmoniesDictionary[key + str(yeses)] = GetHarmoniesForDataBase(ChooseSoundToPlay())
        yeses += 1

    while yeses < numOfHarmonies:
        aud = DetectAnySound()
        temp = GetHarmoniesOfInput(aud, True)
        print(temp)
        answer2 = input("Would you like to save this sound? [Y/N, E to break the recording]\n")
        if answer2 == 'Y' or answer2 == 'y':
            HarmoniesDictionary[key + str(yeses)] = temp
            yeses += 1
        if answer2 == 'E' or answer2 == 'e':
            answer3 = input("Would you like to continue recording? [Y/N]\n")
            if answer3 == 'N' or answer3 == 'n':
                break

    print(HarmoniesDictionary)
    with open('HarmoniesDB.npy', 'wb') as file:
        pickle.dump(HarmoniesDictionary, file)

def GetHarmoniesForDataBase(path):
    # First, we read the audio from the wav:
    samplingRate, audio = wavfile.read(path)

    # Then, we normalize and remove the DC offset:
    audio = abs(audio[:, 1] / np.max(abs(audio[:, 1])))
    audio -= np.mean(audio)

    # We FFT it:
    audio = np.fft.fft(audio)
    bins = np.fft.fftfreq(len(audio))

    # Then we finally get the frequencies in which there are spikes:
    spikes = [x for x in range(0, len(audio)) if audio[x] > 0.2 * np.max(audio) and bins[x] > 0.002]
    spikesFreqs = []
    intervals = []  # We will need it later...
    for x in range(0, len(spikes)):
        if x > 0 and bins[spikes[x]] - bins[spikes[x - 1]] > 0.0001:
            spikesFreqs.append(bins[spikes[x - 1]])
            intervals.append(bins[spikes[x]] - bins[spikes[x - 1]])  # We will need it later...

    # Considering only cases in which there were actual harmonies:
    if not len(spikes) < 1:
        spikesFreqs.append(bins[spikes[len(spikes) - 1]])  # Adding the last harmony

        # Now, we want to save not the list of harmonies, but its length, the interval between them, and the fundemental:
        fundemental = min(spikesFreqs)
        if len(intervals) == 0:
            interval = 0
        else:
            interval = np.mean(intervals)
        length = len(spikesFreqs)
        return [fundemental, interval, length]

    # Else, we return no info:
    return [0, 0, 0]

def GetHarmoniesOfInput(audio, plotSpikes = None):

    # We check if we want to see the spikes:
    if plotSpikes:
        PlotSound(audio)

    # We constantly compare harmonies when using DetectPianoSound, but we start with an empty array. So we don't actually want to compare anything in that case:
    if len(audio) == 0:
        return [0, 0, 0]

    # We preprocess the audio input:
    audio = np.array(audio[0])
    audio = abs(audio[:, 1] / np.max(abs(audio[:, 1])))
    audio -= np.mean(audio)

    # We FFT it:
    audio = np.fft.fft(abs(audio))
    bins = np.fft.fftfreq(len(audio))

    # Then we finally get the frequencies in which there are spikes:
    spikes = [x for x in range(0, len(audio)) if audio[x] > 0.045 * np.max(audio) and bins[x] > 0.002]
    spikesFreqs = []
    intervals = []  # We will need it later...
    for x in range(0, len(spikes)):
        if x > 0 and bins[spikes[x]] - bins[spikes[x - 1]] > 0.8 * bins[spikes[0]]:
            spikesFreqs.append(bins[spikes[x - 1]])
            intervals.append(bins[spikes[x]] - bins[spikes[x - 1]])  # We will need it later...

    # Considering only cases in which there were actual harmonies:
    if not len(spikes) < 1:
        spikesFreqs.append(bins[spikes[len(spikes) - 1]])  # Adding the last harmony

        # Now, we want to save not the list of harmonies, but its length, the interval between them, and the fundemental:
        fundemental = min(spikesFreqs)
        if len(intervals) == 0:
            interval = 0
        else:
            interval = np.min(intervals)
        length = len(spikesFreqs)

        return [fundemental, interval, length]

    # Else, we return no info:
    return [0, 0, 0]

def CompareHarmonies(dic, input):

    # We constantly compare harmonies when using DetectPianoSound, but we start with an empty array. So we don't actually want to compare anything in that case:
    if input[2] < 2:
        return False

    # If the input has way more harmonies than the harmonies in any of the keys, then this must mean that it wasn't a key that was played:
    for key, note in dic.items():
        if note[2] - 2 <= input[2] <= note[2] + 2 and 0.9 * note[1] <= input[1] <= 1.1 * note[1] and 0.9 * note[0] <= input[0] <= 1.1 * note[0]:
            print(key)
            return True

    return False

