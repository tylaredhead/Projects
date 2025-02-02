from constants import *
from math import atan2, degrees, cos, sin, radians, pi
import os 

class CircularQueue:
    fixedSize = 25
    def __init__(self, initialData = []):
        self.__data = [""]*CircularQueue.fixedSize

        self.__frontPointer = 0
        self.__backPointer = -1
        self.__noOfElements = 0

        for element in initialData:
            self.push(element)

    def push(self, element):
        if not self.isFull():
            self.__noOfElements += 1
            self.__backPointer = (self.__backPointer + 1)%(CircularQueue.fixedSize)
            self.__data[self.__backPointer] = element

    def remove(self):
        if not self.isEmpty():
            element = self.peek()
            self.__noOfElements -= 1
            self.__frontPointer = (self.__frontPointer + 1) % (CircularQueue.fixedSize)
            return element
        return False

    def peek(self):
        if not self.isEmpty():
            return self.__data[self.__frontPointer]

    def isFull(self):
        if self.__noOfElements == CircularQueue.fixedSize:
            return True
        return False

    def isEmpty(self):
        if self.__noOfElements == 0:
            return True
        return False 

class Line:
    allImagesQueue = CircularQueue([pg.image.load(os.path.join("Images", "blueRect.png")).convert_alpha(),
                             pg.image.load(os.path.join("Images", "greenRect.png")).convert_alpha(),
                             pg.image.load(os.path.join("Images", "pinkRect.png")).convert_alpha(),
                             pg.image.load(os.path.join("Images", "purpleRect.png")).convert_alpha(),
                             pg.image.load(os.path.join("Images", "orangeRect.png")).convert_alpha()])
    
    def __init__(self, startX, startY, endX, endY, onlyBlackLines = False, lineThickness = 4):
        # Allows variable or fixed colour to be drawn onto the screen
        if not onlyBlackLines:
            self.__originalImg = Line.allImagesQueue.peek()
        else:
            self.__originalImg = pg.image.load(os.path.join("Images", "Arrow-stem.png")).convert_alpha()

        self.__startX, self.__startY = startX, startY
        self.__endX, self.__endY = endX, endY

        self.__changeInX, self.__changeInY = endX - startX, endY - startY

        # PG has positive axis in (i, -j), so angle needs to go anti-cw instead of cw
        self.__length = self.__findLength()
        self.__angle = self.__findAngle()
        self.__lineThickness = lineThickness

        # Allows rescaling and rotation of original imagine rather than an image with existing changes
        image = self.__scaleImg(self.__length, self.__lineThickness, self.__originalImg)
        self.__img = self.__rotateImg(image, -self.__angle)       

        self.__fixed = False

    @staticmethod
    def changeNextColour():
        img = Line.allImagesQueue.remove()
        Line.allImagesQueue.push(img)

    @staticmethod
    def __scaleImg(newX, newY, image):
        return pg.transform.scale(image, (newX, newY))

    @staticmethod
    def __rotateImg(image, angle):
        return pg.transform.rotate(image, angle)

    def __findLength(self):
        return int(((self.__changeInX**2) + (self.__changeInY**2))**0.5)
    
    def __findAngle(self):
        # Checks if grad is undefined
        if self.__changeInX == 0:
            if self.__changeInY > 0:
                return 90
            else:
                return -90
        else:
            return degrees(atan2(self.__changeInY, self.__changeInX))

    def updatePos(self, X, Y):
        # Only updates if start coordinates is not equal to end coordinates
        if X != self.__startX or Y != self.__startY:
            self.__endX, self.__endY = X, Y
            self.__changeInX = self.__endX - self.__startX
            self.__changeInY = self.__endY - self.__startY
        
            self.__length = self.__findLength()
            self.__angle = self.__findAngle()

            image = self.__scaleImg(self.__length, self.__lineThickness, self.__originalImg)
            self.__img = self.__rotateImg(image, -self.__angle)

    def shiftLineHorizontally(self, newStartX):
        self.__startX = newStartX
        self.__endX = self.__startX + self.__changeInX

    def setFixed(self):
        self.__fixed = True    
        
    def draw(self):
        X = self.__startX + self.__changeInX/2 - self.__img.get_width()/2
        Y = self.__startY + self.__changeInY/2 - self.__img.get_height()/2
        SCREEN.blit(self.__img, (X, Y))

    def getFixed(self):
        return self.__fixed

    def getStartCoords(self):
        return [self.__startX, self.__startY]

    def getEndCoords(self):
        return [self.__endX, self.__endY] 
