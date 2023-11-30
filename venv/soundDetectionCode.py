# Libraries and script import
import cv2
import numpy as np
import sounddevice as sd
from noteRecognitionCode import *

# Flags initialization
heard = False
adio = []
ItIsItayRimmlersComputer = True


# This function detects whether a sound was heard and if it was, then it returns it
def DetectSound():
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
    return adio[0]

def audioCallback(audio, frames, time, status):
    frames = 0.001
    if (audio > 0.1).any():
        global heard
        heard = True
        global adio
        adio.append(audio)
