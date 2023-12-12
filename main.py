# Welcome to SheetReader, the program that lets you upload a pdf to assets/ and from then, it will pass you your pdf
# sheet pages automatically

# Libraries:

from pdfOpeningCode import *
from soundAnalysingCode import *
from soundDetectionCode import DetectPianoSound
import pickle

#    Experiment 1: Trying to Save Harmonies and See If It's a Piano

# We record a new dictionary:
SaveHarmoniesForDataBase()

# Then we load:
with open('HarmoniesDB.npy', 'rb') as file:
    HarmoniesDictionary = pickle.load(file)

# We continue recording how many times we want:
for i in range(1):
    SaveHarmoniesForDataBase(HarmoniesDictionary)

# Then we check:
print("Checking whether the next sound you play is a note that was saved:")
DetectPianoSound(HarmoniesDictionary)

#    Experiment 2: Note Detection in Image Domain
#
# # Choosing a file:
# myFile = ChooseFile()
#
# # Processing the file:
# pngs, pngNames = ProcessFile(myFile)
#
# # Presenting the file:
# OpenFile(pngs, pngNames)

