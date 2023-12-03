# Welcome to SheetReader, the program that lets you upload a pdf to assets/ and from then, it will pass you your pdf
# sheet pages automatically

# Libraries:

from pdfOpeningCode import *
from soundAnalysingCode import *
import pickle

#    Experiment 1: Harmony Detection and Comparison

# We save a database of harmonies of piano notes as dictionaries:
#HarmoniesDictionary = {}
#for x in range(2):
#    temp = ChooseSoundToPlay()
#    if x == 0:
#        HarmoniesDictionary['G'] = GetHarmoniesForDataBase(temp)
#    else:
#        HarmoniesDictionary['F'] = GetHarmoniesForDataBase(temp)

#with open('HarmoniesDB.npy', 'wb') as file:
#    pickle.dump(HarmoniesDictionary, file)

# We load the database:
with open('HarmoniesDB.npy', 'rb') as file:
    HarmoniesDictionary = pickle.load(file)

# We get an input audio:
print("Please record you sound and let's see if it's a piano's G or an F:")
temp2 = DetectSound()
mySound = GetHarmoniesOfInput(temp2)

# Let's see it's harmonies:
print([round(spike, 3) for spike in mySound])

# And let's see if it matches to any of the harmonies in the database:
print(CompareHarmonies(HarmoniesDictionary, mySound))


#    Experiment 2: Note Detection

# Choosing a file:
myFile = ChooseFile()

# Processing the file:
pngs, pngNames = ProcessFile(myFile)

# Presenting the file:
OpenFile(pngs, pngNames)

