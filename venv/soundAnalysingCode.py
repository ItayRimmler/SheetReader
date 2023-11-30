import python3_midi as p3m
import os

def ChooseMidiToPlay():
    print("Choose the number of the file you'd like to load:")
    assets = os.listdir('assets/Midi Notes')
    num = 0
    itemsInAssets = []
    for compos in assets:
        num = num + 1
        composNum = str(num)
        itemsInAssets.append(compos)
        print(composNum + " - " + compos + "\n")

    whichAsset = input()
    whichAsset = int(whichAsset)
    name = 'assets/Midi Notes/' + itemsInAssets[whichAsset - 1]
    return name

def PlayMidi(midiPath):
    midi = p3m.read_midifile(midiPath)
    print(midi)

