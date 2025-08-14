import pygame as pg
import Sudoko
from copy import deepcopy
from time import time
from Db_access import addEvent, getLeaderboard

pg.init()

SCREENWIDTH, SCREENHEIGHT = 608, 700

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255, 0,0)
TURQUOISE = (0, 153, 153)
GREY = (220,220,220)
GREEN = (0,255,0)

screen = pg.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
screen.fill(BLACK)

pg.display.set_caption("SUDOKU")
img = pg.image.load('icon.png')
pg.display.set_icon(img)

pg.font.init()
TITLEFONT = pg.font.SysFont("impact", 60)
NUMFONT = pg.font.SysFont("comicsans", 30)
LETTERFONT = pg.font.SysFont("impact", 30)


SQUAREHEIGHT, SQUAREWIDTH = 63, 63        

def getInputBoxes(Grids):
    startX, startY = 5, 5
    ChangePos, DivGap = 66, 3
        
    inputBoxesArr = []
    for row in range(9):
        for col in range(9):
            if Grids.locationEmpty(row, col):
                inputBox = inputBoxesNum(startX+(col*ChangePos)+DivGap*(col//3),startY+(row*ChangePos)+DivGap*(row//3),SQUAREHEIGHT, SQUAREWIDTH, row, col)
            else:
                inputBox = inputBoxesNum(startX+(col*ChangePos)+DivGap*(col//3),startY+(row*ChangePos)+DivGap*(row//3),SQUAREHEIGHT, SQUAREWIDTH, row, col, Grids.getValue(row, col))
            inputBoxesArr.append(inputBox)

    return inputBoxesArr

def compareGrids(Grids):
    errors, correct = [], []
    for row in range(9):
        for col in range(9):
            if Grids.compare(row, col):
                errors.append((row*9)+col)
            else:
                correct.append((row*9)+col)
    return errors, correct

def getTime(Time):
    if Time < 60:
        return f"{round(Time % 60)}s"
    elif Time < 3600:
        return f"{int(Time // 60)}m {round(Time % 60)}s"
    else:
        return f"{int(Time // 3600)}h {int((Time // 60) % 60)}m {round(Time % 60)}s"

def renderTable(y, text):
        box1 = Button(50, y, 75,50, text[0])
        box1.draw(screen)
        box2 = Button(125, y, 300,50, text[1])
        box2.draw(screen)
        box3 = Button(425, y, 125,50, text[2])
        box3.draw(screen)

class Sudoku:
    def __init__(self, unsolvedGrid, UserGrid, solvedGrid):
        self.UserGrid = UserGrid
        self.unsolvedGrid = unsolvedGrid
        self.solvedGrid = solvedGrid

    def updateUserGrid(self, row, col, val):
        self.UserGrid[row][col] = val

    def checkGrid(self, row, col, val):
        return not Sudoko.checkRows(row, col, val, self.UserGrid) or not Sudoko.checkColumns(row, col, val, self.UserGrid) or not Sudoko.checkSector(row, col, val, self.UserGrid)

    def locationEmpty(self, row, col):
        if self.UserGrid[row][col] == 0:
            return True
        return False

    def getValue(self, row, col):
        return str(self.UserGrid[row][col])

    def compare(self, row, col):
        if self.UserGrid[row][col] != self.solvedGrid[row][col]:
            return True
        return False

    def reset(self):
        self.UserGrid = deepcopy(self.unsolvedGrid)

    def solve(self):
        self.UserGrid = deepcopy(self.solvedGrid)
        
class Border:
    def __init__(self, x, y, w, h, colour = WHITE):
        self.rect = pg.Rect(x, y, w, h)
        self.colour = colour 

    def draw(self):
        pg.draw.rect(screen, self.colour, self.rect, 4, border_radius = 5)
        
class Button(Border):
    def __init__(self, x, y, w, h, text):
        super().__init__(x, y, w, h)

        self.text = text
        self.label = LETTERFONT.render(self.text, 1, WHITE)
        self.textRect = self.label.get_rect(center = self.rect.center)
        self.hover = False

        self.clicked = False
        self.error = False

    #hover, click
    def handleEvents(self, eventList):
        pos = pg.mouse.get_pos()
    
        if pos[0] > self.rect.x and pos[0] < self.rect.x + self.rect.w and pos[1] > self.rect.y and pos[1] < self.rect.y + self.rect.h:
            self.hover = True
        else: self.hover = False

        #True for board reset and False if not
        for event in eventList:
            if event.type == pg.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
                self.clicked = True
                return True
        self.clicked = False
        return False

    def getErrorStatus(self):
        return self.error

    def setError(self):
        self.error = not self.error
    
    def getStatus(self):
        return self.clicked

    def updateColour(self, rectColour1, rectColour2, textColour):
        pg.draw.rect(screen, rectColour1, self.rect, border_radius = 5)
        pg.draw.rect(screen, rectColour2, self.rect, 3, border_radius = 5)
        self.label = LETTERFONT.render(self.text, 1, textColour)
        self.textRect = self.label.get_rect(center = self.rect.center)
    
    def draw(self, screen):
        if self.hover:
            self.updateColour(WHITE, TURQUOISE, BLACK)
        else:
            self.updateColour(TURQUOISE, WHITE, WHITE)
        screen.blit(self.label, self.textRect)

class inputBoxes:#use inheritance for specific num values 
    def __init__(self, x, y, w, h, text = ''):
        self.rect = pg.Rect(x, y, w, h)
        
        self.text = text
        self.label = LETTERFONT.render(self.text, 1, BLACK)

        self.active = False

    def setDefault(self):
        if not self.active and self.text == "":
            self.label = LETTERFONT.render("Username", 1, GREY)

    def updateInputChar(self, eventList):
        for event in eventList:
            if event.type == pg.MOUSEBUTTONDOWN and not self.active:
                self.active = self.rect.collidepoint(event.pos)
            elif event.type == pg.MOUSEBUTTONDOWN:
                self.active = not self.active
            if event.type == pg.KEYDOWN and self.active:
                if event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key == pg.K_RETURN:
                    self.active = False
                elif self.label.get_width() < self.rect.w-30:
                    self.text += event.unicode

                self.label = LETTERFONT.render(self.text, 1, BLACK)

    def getUsername(self):
        return self.text

    def draw(self,screen):
        pg.draw.rect(screen, TURQUOISE, self.rect, border_radius = 5)
        pg.draw.rect(screen, WHITE, self.rect, 3, border_radius = 5)
        screen.blit(self.label, (self.rect.x+5,self.rect.y+5))
    
    

class inputBoxesNum(inputBoxes):
    def __init__(self, x, y, w, h, row, col, text = ''):
        super().__init__(x, y, w, h)
        
        self.row = row
        self.col = col       
        
        self.text = text
        self.label = NUMFONT.render(text, 1, BLACK)
        if text == '':
            self.fixedNum = False
        else:
            self.fixedNum = True

        self.active = False
        self.error = False

    def updateInputBoxNum(self, eventList, Grids):
        for event in eventList:
            if event.type == pg.MOUSEBUTTONDOWN and not self.active:
                self.active = self.rect.collidepoint(event.pos)
            elif event.type == pg.MOUSEBUTTONDOWN:
                self.active = not self.active
            if event.type == pg.KEYDOWN and self.active and not self.fixedNum:
                self.error = False
                if event.key == pg.K_BACKSPACE:
                    self.updateLabel("")
                elif event.key == pg.K_1:
                    self.updateLabel("1")
                elif event.key == pg.K_2:
                    self.updateLabel("2")
                elif event.key == pg.K_3:
                    self.updateLabel("3")
                elif event.key == pg.K_4:
                    self.updateLabel("4")
                elif event.key == pg.K_5:
                    self.updateLabel("5")
                elif event.key == pg.K_6:
                    self.updateLabel("6")
                elif event.key == pg.K_7:
                    self.updateLabel("7")
                elif event.key == pg.K_8:
                    self.updateLabel("8")
                elif event.key == pg.K_9:
                    self.updateLabel("9")

        if self.text == '':
            Grids.updateUserGrid(self.row, self.col, 0)
        else:
            Grids.updateUserGrid(self.row, self.col, int(self.text))
            
        if self.active:
            return (9*self.row)+ self.col
        return False

    def updateActive(self):
        self.active = False
                
    def updateLabel(self, text, colour = BLACK):
        self.label = NUMFONT.render(text, 1, colour)
        self.text = text

    def updateErrors(self):
        self.error = True
        if self.text != "":
            self.label = NUMFONT.render(self.text, 1, RED)

    def updateFixedValue(self):
        self.fixedNum = True
        self.label = NUMFONT.render(self.text, 1, BLACK)
        
    def checkDuplicates(self, Grids):
        if self.text != '' and not self.fixedNum:
            if Grids.checkGrid(self.row, self.col, int(self.text)):
                self.label = NUMFONT.render(self.text, 1, RED)
            elif not self.error:
                self.label = NUMFONT.render(self.text, 1, BLACK)
                
    def draw(self,screen):
        if self.text == "":
            pg.draw.rect(screen,WHITE, self.rect)
        else:
            pg.draw.rect(screen,TURQUOISE, self.rect)
        screen.blit(self.label, (self.rect.x+20,self.rect.y+15))

class GameState():    
    def __init__(self):
        self.state = 'intro'

    def intro(self, readyButton, UsernameBox, Grids):
        eventList = pg.event.get()
        for event in eventList:
            if event.type == pg.QUIT:
                running = False

        if readyButton.getErrorStatus():
            pg.time.delay(1000)
            readyButton.setError()
            

        greeting = "Welcome to Sudoko"
        Label = TITLEFONT.render(greeting, 1, WHITE)
        screen.blit(Label, (70, 100))

        UsernameBox.setDefault()
        UsernameBox.updateInputChar(eventList)
        UsernameBox.draw(screen)
        Text = UsernameBox.getUsername()

        if Text == "" and readyButton.handleEvents(eventList):        
            errorLabel = LETTERFONT.render("Must enter a username!", 1, RED)
            screen.blit(errorLabel, (175, 600))
            readyButton.setError()

        ready = readyButton.handleEvents(eventList)
        readyButton.draw(screen)
        if ready and not readyButton.getErrorStatus():
            self.state = "main_game"
            time1 = time()
            return time1
 
    def main_game(self, inputBoxesArr, resetButton, checkButton, solveButton, time1, Grids):
        eventList = pg.event.get()
        for event in eventList:
            if event.type == pg.QUIT:
                running = False
                
        for box in inputBoxesArr:
            Id = box.updateInputBoxNum(eventList, Grids)
 
            box.checkDuplicates(Grids)
            box.draw(screen)

        if Id != False:
            for Idx, box in enumerate(inputBoxesArr):
                if Idx != Id:
                    box.updateActive()
        
        time2 = time()
        Time = getTime(time2 - time1)
        Label = LETTERFONT.render("Time: "+ str(Time) , 1, WHITE)
        screen.blit(Label, (390, 630))

        Reset = resetButton.handleEvents(eventList)
        resetButton.draw(screen)
        if Reset:
            Grids.reset()
            inputBoxesArr = getInputBoxes(Grids)

        Solve = solveButton.handleEvents(eventList)
        solveButton.draw(screen)
        if Solve:
            Grids.solve()
            inputBoxesArr = getInputBoxes(Grids)
            for box in inputBoxesArr:
                box.draw(screen)
                
            self.state = "outro"

        Check = checkButton.handleEvents(eventList)
        checkButton.draw(screen)
        if Check:
            errors, correct = compareGrids(Grids)
            for Idx, box in enumerate(inputBoxesArr):
                if Idx in errors:
                    box.updateErrors()
                elif Idx in correct:
                    box.updateFixedValue()

                if len(errors) == 0:
                    self.state = "outro"
                    return round(time2- time1), inputBoxesArr
        
        return time1, inputBoxesArr
        
    def outro(self, Time, SolveButton, UsernameBox):
        startY = 250
        
        if not SolveButton.getStatus():
            Label = LETTERFONT.render(f"Your Time is {getTime(Time)}!", 1, TURQUOISE)
            screen.blit(Label, (210, 80))

            addEvent(UsernameBox.getUsername(), Time)

        Label = TITLEFONT.render("Leaderboard" , 1, WHITE)
        screen.blit(Label, (150, 150))
        
        Leaderboard = getLeaderboard()
        Usernames = [result[0] for result in Leaderboard]
        Times = [result[1] for result in Leaderboard]
        renderTable(startY, ["Rank", "Username", "Time(s)"])
        
        for i in range(len(Usernames)):
            renderTable(((i+1)*50)+startY, [str(i+1), Usernames[i], Times[i]])        
      
    def findState(self):
        return self.state

    def stateManager(self, inputBoxesArr, resetButton, checkButton, solveButton, time1, Grids, readyButton, UsernameBox):
        if self.state == "intro":
            time1 = self.intro(readyButton, UsernameBox, Grids)
        elif self.state == 'main_game':
            time1, inputBoxesArr = self.main_game(inputBoxesArr, resetButton, checkButton, solveButton, time1, Grids)
        elif self.state == "outro":
            self.outro(time1, solveButton, UsernameBox)
        return time1, inputBoxesArr

    def __str__ (self):
        return f"{self.state}"
    
def main(unsolvedGrid, UserGrid, solvedGrid):
    gameState = GameState()
    
    clock = pg.time.Clock()
    
    readyButton = Button(SCREENWIDTH//2-100, (SCREENHEIGHT*2)//3, 200, 50, "READY!")
    UsernameBox = inputBoxes(SCREENWIDTH//3-50,SCREENHEIGHT//3+60,300, 50)
    border = Border(0, 0, SCREENWIDTH, SCREENHEIGHT)

    Grids = Sudoku(unsolvedGrid, UserGrid, solvedGrid)
    inputBoxesArr = getInputBoxes(Grids)
    resetButton = Button(25, 625, 100, 50, "RESET")
    checkButton = Button(150, 625, 100, 50, "CHECK")
    solveButton = Button(275, 625, 100, 50, "SOLVE")

    #change so when intro ends
    time1 = 0

    running = True
    while running:
        screen.fill(BLACK)
        #if gameState.findState() != "main_game":
            #pg.draw()
        
        if gameState.findState() == "outro":
            pg.time.delay(2000)
            running = False

        time1, inputBoxesArr = gameState.stateManager(inputBoxesArr, resetButton, checkButton, solveButton, time1, Grids, readyButton, UsernameBox)
              
        clock.tick(30)
            
        pg.display.flip()
        pg.time.delay(10)


if __name__ == '__main__':
    unsolvedGrid, UserGrid, solvedGrid = Sudoko.main()
    main(unsolvedGrid, UserGrid, solvedGrid)
