from soundDetectionCode import *
from enum import Enum, auto
from fileAnalysingCode import RightTraveller, Kernel
import matplotlib.pyplot as plt


# This is the part where I recognize the note by sound:
def CharacterizeSound(audio):
    pass

class Note(Enum):
    DO = 1
    RE = 2
    MI = 3
    FA = 4
    SOL = 5
    LA = 6
    SI = 7
    DO2 = 8
    RE2 = 9
    MI2 = 10
    FA2 = 11
    SOL2 = 12
    NONE = 0

def InsertNote(num):
    if num == 6:
        return Note.DO
    elif num == 6.5:
        return Note.RE
    elif num == 5:
        return Note.MI
    elif num == 5.5:
        return Note.FA
    elif num == 4:
        return Note.SOL
    elif num == 4.5:
        return Note.LA
    elif num == 3:
        return Note.SI
    elif num == 3.5:
        return Note.DO2
    elif num == 2:
        return Note.RE2
    elif num == 2.5:
        return Note.MI2
    elif num == 1:
        return Note.FA2
    elif num == 1.5:
        return Note.SOL2
    else:
        return Note.NONE
