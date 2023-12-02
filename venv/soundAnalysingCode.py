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

def GetHarmonies(path):

    # First, we read the audio from the wav:
    _ , audio = wavfile.read(path)

    # Then, we normalize and remove the DC offset:
    audio = abs(audio[:, 1] / np.max(abs(audio[:, 1])))
    audio -= np.mean(audio)

    #
    fft_result = np.fft.fft(audio)
    frequency_bins = np.fft.fftfreq(len(fft_result))
    print(frequency_bins)
    index_to_ignore = int(len(frequency_bins)/2)
    plt.plot(frequency_bins[:index_to_ignore], np.abs(fft_result[:index_to_ignore]))
    plt.show()
