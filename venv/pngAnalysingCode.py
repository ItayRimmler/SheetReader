# Libraries:
import numpy as np
import cv2
from noteRecognitionCode import InsertNote

# MAIN FUNCTIONS:

# This function marks the staff in red. that way, we could debug easily, and afterwards ask the program to delete all that is red. But most importantly, we use this function
# to map our image, and discover where the staff is, how many staves there are, and what is the level of each staff.
def StaffMark(im):
    # This function gets a RightTraveller, which is a coursor like object, makes him walk over the png, and see where the
    # staff is.

    # Setup:
    staff = []
    map = np.full((im.shape), np.array([-1, -1, -1]), dtype=object) # The RightTraveller has a map, in the same size as
    marker = RightTraveller(map=map)                                # the image. He will mark on it the staff
    continueWalking = True
    walkingT = Thermometer(maxHeat=((marker.getMapDim()[0] * marker.getMapDim()[1])+5)) # Thermometer is basically an
    getGap = False                                                                      # iterator that checks if we
    tempGap = 0                                                                         # iterated too much and returns
    i = 1                                                                               # a corresponding boolean
    j = 1

    # The main loop:
    while continueWalking and not walkingT.looped2Much():

        # k is an iterator that we shall use later. points is an array that we will use later:
        k = 0
        points = []

        # We check whether we reached a level 5 staff, and if we did:
        if i == 6:

            for point in maybeStaff:  # We create a sixth staff under level 5
                newPoint = np.array([point[0] + gap, point[1]])
                im[tuple(newPoint)] = np.array([0, 0, 255])
                points.append(newPoint)
            points = np.array(points)
            staffTemp = Staff(coor=points, gap=gap)

            # We make sure to update tempGap after using it:
            tempGap = staffTemp.coor[0][0]

            # We update the .level and .groupNumber fields to the new staff:
            staffTemp + i
            staffTemp * j

            # We add the new object to the staff array:
            staff.append(staffTemp)

            # We tell the marker to skip the staff we just marked:
            marker + (maybeStaff[-1][1] - maybeStaff[0][1])

            i = 1  # ... we again initialize the level flag
            j += 1  # ... we advance our groupNumber flag
            getGap = False  # ... we tell the program to not calculate the gap between the current and previous staff

        # We check if marker is currently on a black pixel, and if it isn't marked as a staff ( [1, 1, 1] on the map):
        if isBlack(im, marker) and not (marker.getUnderUrFeet() == 1).all():

            # We check if it's a staff that we're on:
            maybeStaff = isStaff(im, marker)
            if type(maybeStaff) == np.ndarray:

                # Sometimes, the staff is thicker that one pixel, but we don't want to save it as a staff. So, we mark it as [1,1,1] without adding it to the staff array:
                marker.red()

                # We check whether below us there's a staff:
                while isBlackByRange(im, [[marker.whereRU()[0] + k, marker.whereRU()[1] + i] for i in range(maybeStaff.shape[0])], 0.4) or isRedByRange(im, [[marker.whereRU()[0] + k, marker.whereRU()[1] + i] for i in range(maybeStaff.shape[0])], 0.4):
                    k += 1
                    if marker.whereRU()[0] + k < marker.getMapDim()[0]: # ... and if there's even a pixel row below us
                        if isBlackByRange(im, [[marker.whereRU()[0] + k, marker.whereRU()[1] + i] for i in range(maybeStaff.shape[0])], 0.4):
                            setLine(im, [[marker.whereRU()[0] + k, marker.whereRU()[1] + i] for i in range(maybeStaff.shape[0])], 1)
                    else:
                        break
                marker.unred()

                # Now for the staff itself. We mark it as [1, 1, 1]:
                marker.setMapLine(im, maybeStaff, 1, [1, 1, 1])

                # We set the beginning of the calculation of the gap as the point on which the staff is on:
                gap = maybeStaff[0][0]

                if getGap:

                    # We subtract from it the previous point and save the staff as a 'Staff' object with the newly calculated gap:
                    gap -= tempGap
                    staffTemp = Staff(coor=maybeStaff, gap=gap)
                else:
                    # Or we just save it as a 'Staff' object with gap == 0:
                    staffTemp = Staff(coor=maybeStaff)

                # We make sure to update tempGap after using it:
                tempGap = maybeStaff[0][0]

                # We update the .level and .groupNumber fields to the new staff:
                staffTemp + i
                staffTemp * j

                # We update the level flag and the getGap flag:
                i += 1
                getGap = True

                # We add the new object to the staff array:
                staff.append(staffTemp)

                # We tell the marker to skip the staff we just marked:
                marker + (maybeStaff[-1][1] - maybeStaff[0][1])

        # We see if we could advance marker further right, and if we can't:
        if not marker + 1:
            marker - marker
            marker.red()
            if not marker + (k + 1):
                continueWalking = False
            marker.unred()
        walkingT + 1

    # We check if we iterated too much:
    if walkingT.looped2Much():
        print("HOT HOT HOT!!!")
        return
    else:
        walkingT.cool()

    # Finally, we return the staff array and the map
    return marker.getMap(), np.array(staff)


# This function makes sure to mark in red everything but the notes, that way, we can delete every red pixel later and then we will stay only with the notes:
def LeaveNotes(im, staff, map):

    # Notes, g-clefs, etc. are always relative to the gap between the staves. So we need the gap as a parameter, and we prefer to work with the highest gap:
    gapEst = max([staf.gap for staf in staff])

    # In order to delete all elements we need to start in what's above the staves and below the staves:
    aboveStaves = staff[0].coor[0][0] - gapEst
    belowStaves = staff[-1].coor[0][0] + gapEst
    im[:aboveStaves, :] = np.array([0, 0, 255])
    im[belowStaves:, :] = np.array([0, 0, 255])

    # Then we move on to what's between the staff groups
    for i in range(len(staff) - 1):
        if staff[i + 1].level == 1 and staff[i].level == 6:
            aboveStaves = staff[i+1].coor[0][0] - int(1.25 * gapEst)
            belowStaves = staff[i].coor[0][0] + int(1.25 * gapEst)
            im[belowStaves:aboveStaves, :] = np.array([0, 0, 255])

    # Then, we measure the thickness of the staves, and see which one is the thickest:
    thickness = 0
    for i in range(1,staff[-1].groupNumber + 1):
        temp = getStaffGroupThickness(staff, i)
        thickness = max(thickness, temp)

    # We set our deleting Kernel to be of height of 4 gaps and 5 thicknesses
    deleter = Kernel(x=int(5 * gapEst + 6 * thickness) + 1, h=5 * gapEst + 6 * thickness, map=map)
    deleter.paintAllBody([0, 0, 255])

    # And, we delete a little bit before and after the notes, and hopefully it worked:
    for staf in staff:
        if staf.level == 3:
            deleter.setWhereRU(staf.coor[-1])
            deleter.red()
            deleter + int(staf.gap / 2)
            deleter.unred()
            for i in range(int(1.5 * gapEst)):
                deleter.stainImage(im)
                deleter - 1
            for i in range(deleter.getMapDim()[1] - deleter.whereRU()[1]):
                deleter.stainImage(im)
                deleter + 1
            if staf.groupNumber == 1:
                deleter.setWhereRU([staf.coor[0][0], staf.coor[0][1] + int(5.5 * gapEst)])
            else:
                deleter.setWhereRU([staf.coor[0][0], staf.coor[0][1] + 4 * gapEst])
            for i in range(deleter.whereRU()[1]):
                deleter.stainImage(im)
                deleter - 1


# This function takes the png with only notes and returns a list of values C, D, E, etc. that represents our notes by order:
def NoteMark(im, map, staff, thickness):

    # Notes are always relative to the gap between the staves. So we need the gap as a parameter, and we prefer to work with the highest gap:
    gapEst = min([staf.gap for staf in staff if not staf.gap == 0])

    # Set up the marking kernel
    marker = Kernel(x=int(1.25 * gapEst) + 1, y=int(1.25 * gapEst) + 1, h=int(2.5 * gapEst), w=int(2.5 * gapEst), map=map)

    # I want to recognize elipses, so let's build parameters for an elipse equation:
    a = 0.49 * gapEst  # Height
    b = 0.8 * gapEst  # Width

    # Now to turn it into a general elipse equation (these are the only global parameters, the rest are individual for each iteration in the main loop):
    th = np.pi/6  # Angle
    A = a ** 2 * (np.sin(th)) ** 2 + b ** 2 * (np.cos(th)) ** 2
    B = 2 * (b ** 2 - a ** 2) * np.sin(th) * np.cos(th)
    C = a ** 2 * (np.cos(th)) ** 2 + b ** 2 * (np.sin(th)) ** 2

    # For debugging, we paint the body and then we shall stain the notes:
    marker.paintAllBody([0, 0, 255])
    marker.paintBody(col=[255, 0, 0], coor=[marker.x, marker.y])
    notes = []

    # The main loop:
    for staf in staff:

        # If the staf coordinate is valid for our kernel:
        if marker.setWhereRU(staf.coor[0]):
            marker.red()
            marker - int(gapEst/2)  # Starting from what's above the staff
            marker.unred()
            for k in range(staf.coor.shape[0]):


                # Setting up the parameters:
                shiftx = marker.whereRU()[0]  # Shift of the x-axis from the (0,0) point
                shifty = marker.whereRU()[1]  # Shift of the y-axis from the (0,0) point
                D = -2 * A * shiftx - B * shifty
                E = -B * shiftx - 2 * C * shifty
                F = A * shiftx ** 2 + B * shiftx * shifty + C * shifty ** 2 - a ** 2 * b ** 2

                # Getting the range of points withing the image that make an elipse (rang) or an elipse with a hole (rangy)
                rang = [np.array([x, y]) for x in range(marker.whereRU()[0] - int(marker.h/2), marker.whereRU()[0] + int(marker.h/2)) for y in range(marker.whereRU()[1] - int(marker.w/2), marker.whereRU()[1] + int(marker.w/2)) if A * x ** 2 + B * x * y + C * y ** 2 + D * x + E * y + F < 0.001]
                rangy = [np.array([x, y]) for x in range(marker.whereRU()[0] - int(marker.h/2), marker.whereRU()[0] + int(marker.h/2)) for y in range(marker.whereRU()[1] - int(marker.w/2), marker.whereRU()[1] + int(marker.w/2)) if A * x ** 2 + B * x * y + C * y ** 2 + D * x + E * y + F < 0.001 and (abs(x - marker.x) > 2 or abs(y - marker.y) > 2)]

                # We're checking whether or not it's black enough, or if it's black with a hole inside:
                if marker.stainImage(im, isBlackByRange(im, rang, 0.8) or isBlackByRange(im, rangy, 0.7)):
                    notes.append([InsertNote(staf.level + 0.5), marker.whereRU()[1], staf.groupNumber])

                # Same check, but if it also has red on it, then we classify it as a note that's on the staff and not in the gap:
                if marker.stainImage(im, (isBlackByRange(im, rang, 0.8) or isBlackByRange(im, rangy, 0.7)) and isRedByRange(im, rang, 0.001)):
                    notes.pop() #                                 0.5                             0.4
                    notes.append([InsertNote(staf.level), marker.whereRU()[1], staf.groupNumber])

                # Checking the next point above the staff:
                marker + 1

            # Moving to the notes that are on the staff and not in a gap (we checked it in the above block too, just in case some notes are on the staff but are mistakenlly
            # recognized as on the staff. For some reason, this is the only mistake happening):
            marker.setWhereRU(staf.coor[0])
            for k in range(staf.coor.shape[0]):

                # Setting up the parameters:
                shiftx = marker.whereRU()[0]  # Shift of the x-axis from the (0,0) point
                shifty = marker.whereRU()[1]  # Shift of the y-axis from the (0,0) point
                D = -2 * A * shiftx - B * shifty
                E = -B * shiftx - 2 * C * shifty
                F = A * shiftx ** 2 + B * shiftx * shifty + C * shifty ** 2 - a ** 2 * b ** 2

                # Getting the range of points withing the image that make an elipse (rang) or an elipse with a hole (rangy)
                rang = [np.array([x, y]) for x in range(marker.whereRU()[0] - int(marker.h/2), marker.whereRU()[0] + int(marker.h/2)) for y in range(marker.whereRU()[1] - int(marker.w/2), marker.whereRU()[1] + int(marker.w/2)) if A * x ** 2 + B * x * y + C * y ** 2 + D * x + E * y + F < 0.001]
                rangy = [np.array([x, y]) for x in range(marker.whereRU()[0] - int(marker.h/2), marker.whereRU()[0] + int(marker.h/2)) for y in range(marker.whereRU()[1] - int(marker.w/2), marker.whereRU()[1] + int(marker.w/2)) if A * x ** 2 + B * x * y + C * y ** 2 + D * x + E * y + F < 0.001 and (abs(x - marker.x) > 2 or abs(y - marker.y) > 2)]

                # We're checking whether or not it's black enough, or if it's black with a hole inside, also if it has red on it:
                if marker.stainImage(im, (isBlackByRange(im, rang, 0.8) or isBlackByRange(im, rangy, 0.7)) and isRedByRange(im, rang, 0.001)):
                    notes.append([InsertNote(staf.level), marker.whereRU()[1], staf.groupNumber])

                # Checking the next point on the staff:
                marker + 1

    # We sort the notes correctly and return them:
    notes = sorted(notes, key=lambda x: (x[2], x[1]))
    return notes
# MINOR FUNCTIONS AND CLASSES:
def isStaff(im, trav):
    travOriginalPosition = trav.whereRU()
    blackCount = 0
    notBlackConsecutive = 0
    staff = []
    trav.unred()

    for i in range(travOriginalPosition[1], trav.getMapDim()[1]):
        if isBlack(im, trav):  # Using isBlackByRange will harm my attempt to append each element to the staff
            blackCount += 1
            staff.append(trav.whereRU())
            notBlackConsecutive = 0
            if not trav + 1:
                break
        else:
            notBlackConsecutive += 1
            if notBlackConsecutive > 0.01 * trav.getMapDim()[1]:
                break
            if not trav + 1:
                break
    omdan = trav.whereRU()[1] - travOriginalPosition[1]
    trav.setWhereRU(travOriginalPosition)
    if blackCount > 0.8 * omdan and omdan > 0.15 * trav.getMapDim()[1]:
        return np.array(staff)
    else:
        return False


def getStaffGroupThickness(staff, i):
    thickness = 0
    us = staff[i].groupNumber
    for staf in staff:
        if staf.groupNumber == us:
            thickness += 1
    return thickness


def isBlack(im, trav):
    if (im[tuple(trav.whereRU())] < 50).all():
        trav.setUnderUrFeet([0, 0, 0])
        return True
    return False


def isBlackByRange(im, range, omdan):
    range = np.array(range)
    blackCount = 0
    for index in range:
        if (im[tuple(index)] < 50).all():
            blackCount += 1
    if omdan * range.shape[0] < blackCount:
        return True
    return False


def isRedByRange(im, range, omdan):
    range = np.array(range)
    redCount = 0
    for index in range:
        if np.array_equal(im[tuple(index)], np.array([0, 0, 255])):
            redCount += 1
    if omdan * range.shape[0] < redCount:
        return True
    return False

def isOdd(num):
    if num % 2 == 0:
        return False
    return True

def setLine(im ,other, axis):  # Given a set of coordinates, 'other', which are in only one axis, and the axis itself, we set map to a certain value
    if axis == 0:
        axisnt = 1
    if axis == 1:
        axisnt = 0
    temp = other[0][axisnt]    # get the row number if axisnt is 0, or the col number if axisnt is 1
    temp1 = other[0][axis]     # get the first row number if axis is 0, or the first col number if axis is 1
    temp2 = other[-1][axis]    # get the last row number if axis is 0, or the last col number if axis is 1
    if axisnt == 0:
        im[temp][temp1:temp2] = np.array([0, 0, 255])
    else:
        im[temp1:temp2][temp] = np.array([0, 0, 255])

class Thermometer:
    def __init__(self, heat = 0, maxHeat = 1000 ,tooHot = False):
        self.heat = heat
        self.maxHeat = maxHeat
        self.tooHot = tooHot
    def __add__(self, other):
        self.heat += other
    def __sub__(self, other):
        self.heat -= other
    def looped2Much(self):
        if self.heat == self.maxHeat:
            self.tooHot = True
        return self.tooHot
    def cool(self):
        self - self.heat

class RightTraveller:
    # RightTraveller is a coursor like object, that moves to the right by default, hence the "Right" in "RightTraveller"
    # x is height, y is width
    def __init__(self, y = 0, x = 0, yored = False, map = []):
        self.map = map
        if x < 0 or y < 0 or x >= map.shape[0] or y >= map.shape[1]:
            print("Illeagal initialization!")
            return
        self.y = y
        self.x = x
        self.yored = yored  # yored == going down in Hebrew

    def __add__(self, other):
        if isinstance(other, RightTraveller):
            if not self.yored:
                if self.y + other.y > -1 and self.y + other.y < self.getMapDim()[1]:
                    self.y += other.y
                    return True
                else:
                    print("Traveller can't go to " + str([self.x, self.y + other.y]))
                    return False
            else:
                if self.x + other.x > -1 and self.x + other.x < self.getMapDim()[0]:
                    self.x += other.x
                    return True
                else:
                    print("Traveller can't go to " + str([self.x + other.x, self.y]))
                    return False
        else:
            if not self.yored:
                if self.y + other > -1 and self.y + other < self.getMapDim()[1]:
                    self.y += other
                    return True
                else:
                    #print("Traveller can't go to " + str([self.x, self.y + other]))
                    return False
            else:
                if self.x + other > -1 and self.x + other < self.getMapDim()[0]:
                    self.x += other
                    return True
                else:
                    print("Traveller can't go to " + str([self.x + other, self.y]))
                    return False

    def __sub__(self, other):
        if isinstance(other, RightTraveller):
            if not self.yored:
                if self.y - other.y > -1 and self.y - other.y < self.getMapDim()[1]:
                    self.y -= other.y
                    return True
                else:
                    print("Traveller can't go to " + str([self.x, self.y - other.y]))
                    return False
            else:
                if self.x - other.x > -1 and self.x - other.x < self.getMapDim()[0]:
                    self.x -= other.x
                    return True
                else:
                    print("Traveller can't go to " + str([self.x - other.x, self.y]))
                    return False
        else:
            if not self.yored:
                if self.y - other > -1 and self.y - other < self.getMapDim()[1]:
                    self.y -= other
                    return True
                else:
                    print("Traveller can't go to " + str([self.x, self.y - other]))
                    return False
            else:
                if self.x - other > -1 and self.x - other < self.getMapDim()[0]:
                    self.x -= other
                    return True
                else:
                    print("Traveller can't go to " + str([self.x - other, self.y]))
                    return False

    def whereRU(self):
        return np.array([self.x, self.y])

    def red(self): # red == go down in Hebrew
        self.yored = True

    def unred(self):
        self.yored = False

    def getYored(self):
        return self.yored

    def getMap(self):
        return np.array(self.map)

    def getMapDim(self):
        return np.array(self.map.shape)

    def getUnderUrFeet(self):  # gives the map value in wherever the traveller is
        return np.array(self.map[tuple(self.whereRU())])

    def setUnderUrFeet(self, other):
        self.map[tuple(self.whereRU())] = np.array(other)

    def setWhereRU(self, other):  # sets the x and y of the traveller
        [self.x, self.y] = np.array(other)

    def setMapLine(self, im ,other, axis, col):  # Given a set of coordinates, 'other', which are in only one axis, and the axis itself, we set map to a certain value
        if axis == 0:
            axisnt = 1
        if axis == 1:
            axisnt = 0
        temp = other[0][axisnt]    # get the row number if axisnt is 0, or the col number if axisnt is 1
        temp1 = other[0][axis]     # get the first row number if axis is 0, or the first col number if axis is 1
        temp2 = other[-1][axis]    # get the last row number if axis is 0, or the last col number if axis is 1
        if axisnt == 0:
            self.map[temp][temp1:temp2] = np.array(col)
            setLine(im, other, axis)
        else:
            self.map[temp1:temp2][temp] = np.array(col)
            setLine(im, other, axis)

    def helloTraveller(self):
        return np.array([self.whereRU(), self.yored, self.map, self.getMapDim()])


class Staff: # Represents the properties of the staff. Has a group number, level between 1-5, coordinates, and the gap between it and the upper staff (if it's in a different
    # group then gap is 0)
    def __init__(self, coor = np.array([]), col = np.array([-1, -1, -1]), level = 0, groupNumber = 0, gap = 0):
        self.coor = coor
        self.col = col
        self.level = level
        self.groupNumber = groupNumber
        self.gap = gap
    def __add__(self, other):
        if isinstance(other, np.ndarray):
            for ele in other:
                print(ele)
                np.append(self.coor,np.array(ele)) # why doesnt it work?
                print(self.coor)
        elif isinstance(other, int):
            self.level += other
    def __mul__(self, other):
        self.groupNumber += other


class Kernel(RightTraveller): # A right traveller surrounded by pixels called body
    def __init__(self, w=3, h=3, x=1, y=1, map=[]):
        self.map = map
        if x < 0 or y < 0 or x >= map.shape[0] or y >= map.shape[1]:
            print("Illegal initialization!")
            return
        self.x = x
        self.y = y
        self.yored = False
        if h >= 1 and w >= 1:
            if isOdd(int(h)):
                self.h = int(h)
            else:
                self.h = int(h - 1)
            if isOdd(int(w)):
                self.w = int(w)
            else:
                self.w = int(w - 1)
        elif h < 1 and w >= 1:
            h = 3
            if isOdd(int(w)):
                self.w = int(w)
            else:
                self.w = int(w - 1)
        elif h >= 1 and w < 1:
            w = 3
            if isOdd(int(h)):
                self.h = int(h)
            else:
                self.h = int(h - 1)
        else:
            h = 3
            w = 3
        if self.bodyInMap():
            self.body = []
            self.frame = []
            for i in range(self.h):
                self.body.append([])
                for j in range(self.w):
                    self.body[i].append(np.array([-1, -1, -1]))
                    if i == 0 or j == 0 or i == self.h - 1 or j == self.w - 1:
                        self.frame.append(np.array([-1, -1, -1]))
            self.body = np.array(self.body)
            self.frame = np.array(self.frame)
        else:
            print("Illegal initialization!")
            self.body = False
            self.frame = False
            return

    def __add__(self, other):
        val = super().__add__(other)
        if not self.bodyInMap() and val:
            super().__sub__(other)
            return False
        return val

    def __sub__(self, other):
        val = super().__sub__(other)
        if not self.bodyInMap() and val:
            super().__add__(other)
            return False
        return val

    def setWhereRU(self, other):
        previousLoc = self.whereRU()
        super().setWhereRU(other)
        if not self.bodyInMap():
            super().setWhereRU(previousLoc)
            return False
        return True

    def bodyInMap(self):
        if self.whereRU()[0] - int(self.h/2) < 0 or self.whereRU()[0] + int(self.h/2) >= self.getMapDim()[0] or self.whereRU()[1] - int(self.w/2) < 0 or self.whereRU()[1] + int(self.w/2) >= self.getMapDim()[1]:
            return False
        return True

    def getBody(self):
        return self.body

    def setBody(self, other):
        print("Choose a pixel to change to :" + str(other) +"\n\n")
        for i in range(self.h):
            for j in range(self.w):
                print(self.body[i][j], end="")
                print("     ", end="")
            print("\n")
        k = input("Please provide row number:\n")
        l = input("And a column number:\n")
        self.body[int(k)][int(l)] = np.array(other)

    def printBody(self):
        for i in range(self.h):
            for j in range(self.w):
                print(self.body[i][j], end="")
                print("     ", end="")
            print("\n")

    def getFrame(self):
        return self.frame

    def paintAllBody(self, col):
        for i in range(self.h):
            for j in range(self.w):
                self.body[i][j] = np.array(col)

    def paintBody(self, col, coor):
        coor = np.array(coor)
        self.body[coor[0]][coor[1]] = np.array(col)

    def stainImage(self, im, condition = True):
        if im.shape[0] < self.h or im.shape[1] < self.w or self.whereRU()[0] < 0 or self.whereRU()[0] >= im.shape[0] or self.whereRU()[1] < 0 or self.whereRU()[1] >= im.shape[1]:
            print("One of the kernels' dimensions is bigger than the corresponding dimension of the image, or the kernel is outside the image. Nothing happened.")
            return False
        if not type(condition) == bool:
            condition = True
        if condition:
            im[self.whereRU()[0] - int(self.h/2):self.whereRU()[0] + int(self.h/2) + 1, self.whereRU()[1] - int(self.w/2):self.whereRU()[1] + int(self.w/2) + 1] = self.getBody()
            return True
