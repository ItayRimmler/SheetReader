# This file functions as a script to open pdf files in 'assets/' and calling the necessary functions to analyse the sheet the sound input and generally
# manage pdf pages presentation.

# Libraries and scripts:
from enum import Enum, auto

import cv2
import fitz, os
from pngAnalysingCode import *
from soundDetectionCode import DetectAnySound

# Flags for later use in multiple functions:
pageNum = 0
previousPage = False  # This flag is unused currently. I'll apply it when I'll have a function that can flip it with a special sound.


def ChooseFile():

    # Presents the list of pdf files in 'assets/':
    print("Choose the number of the file you'd like to load:\n")
    assets = os.listdir('assets')
    num = 0
    itemsInAssets = []
    for compos in assets:
        if compos[-3:] == "pdf":
            num = num + 1
            composNum = str(num)
            itemsInAssets.append(compos)
            print(composNum + " - " + compos + "\n")

    # Choosing from within the list of pdf files
    whichAsset = int(input())
    name = 'assets/' + itemsInAssets[whichAsset - 1]
    return name


# KEY TO UNDERSTANDING THE VARIABLES IN THE FOLLOWING FUNCTIONS (you don't need to memorize this, just return here if you can't follow the code):
# Variables used with fitz's functions:
# 1. sheet - our chosen pdf
# 2. sheetPage - our desired page within 'sheet'
# 3. sheetImage - the png version of 'sheetPage'
# Variables used with OpenCV's functions:
# 4. loadedImage - the representation of 'sheetImage' in OpenCV terms. In other words, we simply read, with OpenCV, the file created and stored within the variable
# 'sheetImage' (that probably has another name in 'assets/'), and saved the read file in 'loadedImage'
# Variables used with pngAnalysingCode:
# 5. map - I use a class that "walks" on my pixel map, and mapping it. It has various and some potential uses, so I keep this variable and return it from functions to
# update it
# 6. staff - an array of 'Staff' objects, containing coordinate of the staff, and many other properties of it
# 7. sheetImageNamePainted - the name of the png file after it has been painted
# Variables used with soundAnalysingCode:
# .8 inputAudio - a variable, unused for now, that stores the input sound made, to later analyse if it was the correct sound
# Variables used to go into intermediate state:
# 9. isIntermediateJustOver - a flag that tells us if we went out from an intermediate state, or we were in a "regular" state
# 10. previousPage - a flag that is raised with a condition that doesn't exist yet, but will be, that says to go back to the previous page (if it's an intermediate state
# then to the corresponding intermediate state)


def ProcessFile(sheetPath):

    # Opening the pdf chosen
    sheet = fitz.open(sheetPath)

    # Accessing the globally defined pageNum and previousPage iterator and flag:
    global pageNum

    # Initializing the png file list that we will return:
    pngList = []
    pathList = []

    # Our main loop that presents each page
    while pageNum < sheet.page_count:

        # We already loaded the pdf file, now to load the correct page:
        sheetPage = sheet.load_page(pageNum)

        # Now to turn it into an analysable png, and let us get its name:
        sheetImage = sheetPage.get_pixmap(matrix=fitz.Matrix(2, 2))  # Here we decide the resolution by the way
        sheetImageName = sheetPath.rstrip('.pdf') + str(pageNum) + '.png'
        sheetImage.save(sheetImageName, 'png')

        # And now we read the new png. We stop using fitz and start using OpenCV:
        loadedImage = cv2.imread(sheetImageName)
        print(loadedImage)
        # Sharpening the image, then saving it:
        sharpeningKernel = np.array([[-1, -1, -1],
                                      [-1, 9, -1],
                                      [-1, -1, -1]])
        loadedImage = cv2.filter2D(loadedImage, -1, sharpeningKernel)
        cv2.imwrite(sheetImageName, loadedImage)

        # We now take the png and extract from it the staff and another useful variable named 'map' for later use. We also remove the initial version as we don't need it anymore:
        sheetImageNamePainted = sheetPath.rstrip('.pdf') + str(pageNum) + 'Painted' + '.png'
        map, staff = StaffMark(loadedImage)
        cv2.imwrite(sheetImageNamePainted, loadedImage)
        os.remove(sheetImageName)

        # Then, we make sure to leave only the notes:
        thickness = LeaveNotes(loadedImage, staff, map)
        cv2.imwrite(sheetImageNamePainted, loadedImage)

        # We then proceed to mark all the notes and classify them:
        notes = NoteMark(loadedImage, map, staff, thickness)  # NEED TO: 1. READ C AND B 2. GET MORE QUARTER ONLY SONGS LIKE YONATHAN 3. MOVE ON TO THE NEXT SUBJECT
        print(notes)

        # The above lines painted everything that we don't want as red. So, we just filter out any red pixels:
        loadedImage = cv2.cvtColor(loadedImage, cv2.COLOR_BGR2GRAY)
        _, loadedImage = cv2.threshold(loadedImage, 70, 255, cv2.THRESH_BINARY)

        # And we find the contours and draw them:
        contours, _ = cv2.findContours(
        loadedImage, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(loadedImage, contours, -1, (0, 0, 255), 2)
        cv2.imwrite(sheetImageNamePainted, loadedImage)

        # Finally, we save each processed image and its path:
        pngList.append(loadedImage)
        pathList.append(sheetImageNamePainted)

        # And we iterate:
        pageNum = pageNum + 1

    sheet.close()
    return pngList, pathList


def OpenFile(loadedImages, imagePaths):

    # Accessing the globally defined pageNum and previousPage iterator and flag:
    global previousPage

    for index, (loadedImage, sheetImageNamePainted) in enumerate(zip(loadedImages, imagePaths)):

        # Continue reading and you will understand this flag. For now, keep in mind that we need to set this value to False:
        isIntermediateJustOver = False

        # We show the image for 1 millisecond, presenting it to the front:
        cv2.imshow("Loaded Image", loadedImage)
        cv2.setWindowProperty("Loaded Image", cv2.WND_PROP_TOPMOST, 1)
        cv2.waitKey(1)

        # We close the image only when a sound is made (we need a function that checks whether it's the correct sound, but we don't have that yet):
        inputAudio = DetectAnySound()  # For now, inputAudio will not be used

        cv2.destroyAllWindows()

        # Here is the logic to going into the intermediate state:
        if not index == len(loadedImages) - 1:
            isIntermediateJustOver = IntermediateState(index, loadedImages, imagePaths)
        else:
            for imageName in imagePaths:
                os.remove(imageName)
        if previousPage:
            previousPage = False
            if not isIntermediateJustOver:
                IntermediateState(index - 1, loadedImages, imagePaths)


def IntermediateState(i, loadedImages, imagesPaths):

    loadedImage = loadedImages[i]
    loadedNextImage = loadedImages[i + 1]
    cv2.imshow("Loaded Image", loadedImage)
    cv2.imshow("Loaded Image2", loadedNextImage)
    cv2.setWindowProperty("Loaded Image", cv2.WND_PROP_TOPMOST, 1)
    cv2.setWindowProperty("Loaded Image2", cv2.WND_PROP_TOPMOST, 1)
    cv2.moveWindow("Loaded Image2", 600, 0)
    cv2.waitKey(1)

    # We close the image only when a sound is made (we need a function that checks whether it's the correct sound, but we don't have that yet):
    inputAudio = DetectAnySound()  # For now, inputAudio will not be used
    cv2.destroyAllWindows()

    return True
