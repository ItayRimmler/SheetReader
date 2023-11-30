# Welcome to SheetReader, the program that lets you upload a pdf to assets/ and from then, it will pass you your pdf
# sheet pages automatically

from pdfOpeningCode import *

myFile = ChooseFile()
pngs, pngNames = ProcessFile(myFile)
OpenFile(pngs, pngNames)
# Presenting my work:

