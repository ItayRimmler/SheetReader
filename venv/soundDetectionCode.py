# Libraries and script import
import cv2
import numpy as np
import sounddevice as sd
from noteRecognitionCode import *
from soundAnalysingCode import CompareHarmonies, GetHarmoniesOfInput
# Flags initialization
heard = False
adio = []
ItIsItayRimmlersComputer = False


# This function detects whether a sound was heard and if it was, then it returns its key:
def DetectPianoSound(dic):
    global adio
    while not CompareHarmonies(dic, GetHarmoniesOfInput(adio)):
        adio = []
        if ItIsItayRimmlersComputer:
            recording = sd.InputStream(device='Microphone Array (Intel® Smart Sound Technology for Digital Microphones), Windows DirectSound', channels=2, callback=audioCallback)
        else:
            recording = sd.InputStream(callback=audioCallback)

        global heard
        heard = False
        recording.start()
        while not heard:
            pass
        recording.stop()
    return adio

def DetectAnySound():
    global adio
    adio = []
    if ItIsItayRimmlersComputer:
        recording = sd.InputStream(device='Microphone Array (Intel® Smart Sound Technology for Digital Microphones), Windows DirectSound', channels=2, callback=audioCallback)
    else:
        recording = sd.InputStream(callback=audioCallback)

    global heard
    heard = False

    recording.start()
    while not heard:
        pass
    recording.stop()
    return adio

def audioCallback(audio, frames, time, status):
    frames = 0.001
    if (audio > 0.05).any():  # You might wanna change that parameter to 0.1... Now it's way to sensitive
        global heard
        heard = True
        global adio
        adio.append(audio)
