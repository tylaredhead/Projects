from constants import *
from GeneralComponents import Line, CircularQueue

class Border:
    def __init__(self, x, y, w, h, colour = BLUE):
        self.__rect = pg.Rect(x, y, w, h)
        self.__colour = colour 

    def draw(self):
        pg.draw.rect(SCREEN, self.__colour, self.__rect)

    def drawOutline(self):
        pg.draw.rect(SCREEN, BLACK, self.__rect, 1)

    def getX(self):
        return self.__rect.x
    
    def getY(self):
        return self.__rect.y
    
    def getW(self):
        return self.__rect.w
    
    def getH(self):
        return self.__rect.h
            
class Button:
    def __init__(self, x, y, w, h, text, colour, phases=1):
        self.__rect = pg.Rect(x, y, w, h)
        self.__y, self.__w, self.__h = y, w, h

        # Sets displayed text depending on number of phases
        self.__phases = phases
        self.__colour = colour
        if self.__phases > 1:
            # self.__text[0] acts as current phase 
            self.__text = CircularQueue(text)
            self.__label = FONT.render(text[0], 1, colour)
            self.__textRect = self.__label.get_rect(center = self.__rect.center)
        else:
            self.__label = FONT.render(text, 1, colour)
            self.__textRect = self.__label.get_rect(center = self.__rect.center)

        self.__hideButton = False
    
    def handleEvents(self, eventList):
        # Determines if button is clicked
        for event in eventList:
            if event.type == pg.MOUSEBUTTONDOWN and self.__rect.collidepoint(event.pos):
                if self.__phases > 1:
                    self.changePhase()
                    return [True, self.__text.peek()]
                return True
        return False  

    def changePhase(self):
        phase = self.__text.remove()
        self.__text.push(phase)
        self.__label = FONT.render(self.__text.peek(), 1, self.__colour)
        self.__textRect = self.__label.get_rect(center = self.__rect.center)

    def draw(self):
        if not self.__hideButton:
            pg.draw.rect(SCREEN, WHITE, self.__rect, border_radius = 5)
            pg.draw.rect(SCREEN, BLACK, self.__rect, 1, border_radius = 5)
            SCREEN.blit(self.__label, self.__textRect)

    def changePos(self, x, y):
        self.__rect = pg.Rect(x, y, self.__w, self.__h)
        self.__textRect = self.__label.get_rect(center = self.__rect.center)

    def setShowButton(self):
        self.__hideButton = False

    def setHideButton(self):
        self.__hideButton = True

    def getIfHidden(self):
        return self.__hideButton
    
    def getY(self):
        return self.__rect.y
    
    def getCurrentPhase(self):
        return self.__text.peek()

class scrollbar:
    ButtonSideLen = 25
    def __init__(self, x, y, w, h, header, maxRecords, pos, tableFormat = [], interval = 1, ifLinesDrawn = False):
        self.__data = []

        self.__x, self.__y = x, y
        self.__w, self.__h = w, h

        # Header acts as a record
        self.__header = header
        self.__startIdx = 0
        self.__maxRecords = maxRecords

        # U: up and down button will be under data, R: up and down buttons will be to the right of the bottom record
        self.__pos = pos
        if pos == "R":
            self.__upButton = Button(x + w, y + h - (2*scrollbar.ButtonSideLen), scrollbar.ButtonSideLen, scrollbar.ButtonSideLen, "Up", BLACK)
            self.__downButton = Button(x + w, y + h - scrollbar.ButtonSideLen, scrollbar.ButtonSideLen, scrollbar.ButtonSideLen, "Down", BLACK)
        elif pos == "U":
            self.__upButton = Button(x + w - (scrollbar.ButtonSideLen), y + h, scrollbar.ButtonSideLen, scrollbar.ButtonSideLen, "Up", BLACK)
            self.__downButton = Button(x + w, y + h, scrollbar.ButtonSideLen, scrollbar.ButtonSideLen, "Down", BLACK)

        # interval ==> enable multiple records added to be considered as one 
        self.__tableFormat = tableFormat
        self.__interval = interval
        
        if tableFormat != []:
            self.__Lines = []
            for i in range(1, len(tableFormat)):
                line = Line(x + tableFormat[i], y + 5*SMALLPAD, x + tableFormat[i], y + h - SMALLPAD, True)
                self.__Lines.append(line)

            lineThickness = 4
            for i in range(maxRecords//interval):
                line = Line(x + SMALLPAD, y + (interval*i + 1.9)*MEDIUMPAD, x + w, y + (interval*i + 1.9)*MEDIUMPAD, True, lineThickness)
                self.__Lines.append(line)
                lineThickness = 2
    
    def insertRecords(self, idx, element, related2LastRecord = False):
        # Handles grouping of records if related to each other
        if self.__maxRecords + self.__startIdx == len(self.__data) and not related2LastRecord:
            if self.__header != "" and self.__startIdx == 0 and self.__interval > 1:
                self.__startIdx += 1
            self.__startIdx += self.__interval
        elif self.__maxRecords + self.__startIdx == len(self.__data):
            self.__startIdx += self.__interval
        if idx == -1:
            self.__data.append(element)
        else:
            self.__data.insert(idx, element)
        
    def delRecord(self, idx):
        self.__data.pop(idx + self.__startIdx)
                
        if self.__startIdx + self.__maxRecords >= len(self.__data) and self.__startIdx != 0:
            self.__startIdx -= 1
        
    def reset(self):
        self.__data = []
        self.__startIdx = 0

        self.__upButton.setHideButton()
        self.__downButton.setHideButton()        

    def findElement(self, element):
        for idx, each in enumerate(self.__data):
            if self.__tableFormat == []:
                if element == each:
                    return idx
            else:
                for column in each:
                    if column in element:
                        return idx

        return False

    def handleEvents(self, eventList): 
        self.__upButton.setHideButton()
        self.__downButton.setHideButton()

        if len(self.__data) > self.__maxRecords:
            if self.__startIdx > self.__interval - 1 and self.__tableFormat == []:
                self.__upButton.setShowButton()
            elif self.__startIdx > self.__interval and self.__tableFormat != []:
                self.__upButton.setShowButton()

            if self.__maxRecords + self.__startIdx <= len(self.__data) - self.__interval and self.__tableFormat == []:
                self.__downButton.setShowButton()
            elif self.__maxRecords + self.__startIdx <= len(self.__data) - self.__interval + 1 and self.__tableFormat != []:
                self.__downButton.setShowButton()

        self.__shiftRecords(eventList)

    def __shiftRecords(self, eventList):
        if self.__downButton.handleEvents(eventList) and not self.__downButton.getIfHidden():
            self.__startIdx += self.__interval
        
        if self.__upButton.handleEvents(eventList) and not self.__upButton.getIfHidden():
            self.__startIdx -= self.__interval

    # Shifts button with scrollbar shift
    def changeX(self, newX):
        self.__x = newX

        if self.__tableFormat != []:
            # Shift for vertical lines
            for i, line in enumerate(self.__Lines[:len(self.__tableFormat) - 1]):
                line.shiftLineHorizontally(newX + self.__tableFormat[i + 1])

            # Shift for horizontal lines
            for line in self.__Lines[len(self.__tableFormat) - 1:len(self.__Lines)]:
                line.shiftLineHorizontally(newX)

        if self.__pos == "R":
            self.__upButton.changePos(self.__x + self.__w, self.__upButton.getY())
            self.__downButton.changePos(self.__x + self.__w, self.__downButton.getY())
        elif self.__pos == "U":
            self.__upButton.changePos(self.__x + self.__w - scrollbar.ButtonSideLen, self.__upButton.getY())
            self.__downButton.changePos(self.__x + self.__w, self.__downButton.getY())

    def updateHeader(self, header):
        self.__header = header

    def display(self):
        self.__upButton.draw()
        self.__downButton.draw()

        if len(self.__data) > 0:
            count = 0
            if self.__header != "":
                self.__dispHeader(self.__header, 0)
                count += 1

            # Allows column headings to be drawn
            if self.__startIdx != 0 and self.__tableFormat != []:
                self.__dispDataAsTable(self.__data[0], count)
                self.__maxRecords -= 1 # Temp decrease to account for headings
                count += 1            
            
            for idx in range(len(self.__data)):
                if idx >= self.__startIdx and idx < self.__startIdx + self.__maxRecords:
                    if self.__tableFormat == []:
                        self.__dispData(self.__data[idx], count)
                    else:
                        self.__dispDataAsTable(self.__data[idx], count)
                    count += 1

            if self.__startIdx != 0 and self.__tableFormat != []:
                self.__maxRecords += 1

            if self.__tableFormat != []:
                self.__displayLines()
                             
    def __dispData(self, element, colIdx):
        if element.lstrip()[:4] == "EDGE":
            label = SMALLFONT.render(element, 1, BLACK)
        else:
            label = FONT.render(element, 1, BLACK)
        SCREEN.blit(label, (self.__x + 10, self.__y + 20*colIdx))

    def __dispDataAsTable(self, elements, colIdx):
        for idx, element in enumerate(elements):
            label = FONT.render(element, 1, BLACK)
            SCREEN.blit(label, (self.__x+10 + self.__tableFormat[idx], self.__y + 20*colIdx))

    def __dispHeader(self, element, colIdx):
        label = TITLEFONT.render(element, 1, BLACK)
        SCREEN.blit(label, (self.__x, self.__y + 20*colIdx))

    def __displayLines(self):
        for lineIdx in range((self.getLenDispData()-1)//self.__interval + len(self.__tableFormat) - 1):
            self.__Lines[lineIdx].draw()

    def getElement(self, idx):
        try:
            return self.__data[idx]
        except IndexError:
            return False
        
    def getLenDispData(self):
        if len(self.__data) < self.__maxRecords:
            return len(self.__data)
        else:
            return self.__maxRecords

    def getLenData(self):
        return len(self.__data)

    def getX(self):
        return self.__x
    
    def getY(self):
        return self.__y
    
    def getW(self):
        return self.__w

    def getH(self):
        return self.__h

    def getStartIdx(self):
        return self.__startIdx

class inputBox:
    def __init__(self, ID, x, y, w, h, defaultTxt, typeOfInput):
        self.ID = ID
        self.__rect = pg.Rect(x, y, w, h)
        
        self.__defaultTxt = defaultTxt
        self.__text = ""
        self.__label = WRITINGFONT.render(self.__text, 1, BLACK)
        self.__textRect = self.__label.get_rect(center = self.__rect.center)

        self.__active = False
        self.__typeOfInput = typeOfInput
        self.__origInputType = typeOfInput
  
    def updateInputs(self, eventList):
        self.__setDefault()
        if self.__typeOfInput == "Int" or self.__typeOfInput == "Float":
            self.__updateInputInt(eventList)
        else:
            self.__updateInputChar(eventList)

    # Sets default values to hint at correct inputs
    def __setDefault(self):
        if not self.__active and self.__text == "":
            self.__label = WRITINGFONT.render(self.__defaultTxt, 1, DARKGREY)
            self.__textRect = self.__label.get_rect(center = self.__rect.center)

    def __updateInputInt(self, eventList):
        for event in eventList:
            if event.type == pg.MOUSEBUTTONDOWN and not self.__active:
                self.__active = self.__rect.collidepoint(event.pos)
                if self.__active:
                    return True
            elif event.type == pg.MOUSEBUTTONDOWN:
                self.__active = not self.__active
                return True 
            if event.type == pg.KEYDOWN and self.__active:
                if event.key == pg.K_BACKSPACE:
                    # If . is removed, reinstate possible . as a user input
                    if len(self.__text) > 0:
                        if self.__text[-1] == ".":
                            self.__typeOfInput = "Float"
                        self.__text = self.__text[:-1]

                if WRITINGFONTLETTERWIDTH*len(self.__text) < self.__rect.w:
                    if event.key == pg.K_1:
                        self.__text += "1"
                    elif event.key == pg.K_2:
                        self.__text += "2"
                    elif event.key == pg.K_3:
                        self.__text += "3"
                    elif event.key == pg.K_4:
                        self.__text += "4"
                    elif event.key == pg.K_5:
                        self.__text += "5"
                    elif event.key == pg.K_6:
                        self.__text += "6"
                    elif event.key == pg.K_7:
                        self.__text += "7"
                    elif event.key == pg.K_8:
                        self.__text += "8"
                    elif event.key == pg.K_9:
                        self.__text += "9"
                    elif event.key == pg.K_0:
                        self.__text += "0"
                    elif self.__typeOfInput == "Float" and event.key == pg.K_PERIOD:
                        # Prevents more than 1 . being entered per number
                        self.__typeOfInput = "Int"
                        self.__text += "."

                self.__label = WRITINGFONT.render(self.__text, 1, BLACK)
                self.__textRect = self.__label.get_rect(center = self.__rect.center)

    def __updateInputChar(self, eventList):
        for event in eventList:
            if event.type == pg.MOUSEBUTTONDOWN and not self.__active:
                self.__active = self.__rect.collidepoint(event.pos)
                if self.__active:
                    return True
            elif event.type == pg.MOUSEBUTTONDOWN:
                self.__active = not self.__active
                return True
            elif event.type == pg.KEYDOWN and self.__active:
                if event.key == pg.K_BACKSPACE:
                    if  len(self.__text)>0:
                        self.__text = self.__text[:-1]
                elif event.key == pg.K_RETURN:
                    self.__active = False
                elif self.__rect.w < 100 and len(self.__text)<2:
                    self.__text += event.unicode
                elif WRITINGFONTLETTERWIDTH*len(self.__text)-20 < self.__rect.w and self.__rect.w >=100:
                    self.__text += event.unicode

                if len(self.__text) > 0:
                    if self.__text[-1] == ":":
                        self.__text = self.__text[:-1]
                        
                self.__label = WRITINGFONT.render(self.__text, 1, BLACK)
                self.__textRect = self.__label.get_rect(center = self.__rect.center)

    def resetTxt(self):
        self.__text = ""
        self.__label = WRITINGFONT.render(self.__text, 1, BLACK)
        self.__textRect = self.__label.get_rect(center = self.__rect.center)

        if self.__origInputType != self.__typeOfInput:
            self.__typeOfInput = self.__origInputType

        self.__active = False

    def resetActive(self):
        self.__active = False

    def draw(self):
        pg.draw.rect(SCREEN, WHITE, self.__rect)
        pg.draw.rect(SCREEN, BLACK, self.__rect, 1)
        SCREEN.blit(self.__label, self.__textRect)

    def getTxt(self):
        return self.__text

    def getDefaultTxt(self):
        return self.__defaultTxt
    
    def getActive(self):
        return self.__active

    def getID(self):
        return self.ID
