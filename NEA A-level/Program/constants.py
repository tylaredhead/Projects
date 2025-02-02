import pygame as pg

pg.init()

SCREENWIDTH, SCREENHEIGHT = 1200, 700

# Colours 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHTGREY = (218, 215, 217)
LIGHTERGREY = (128, 128, 128)
DARKGREY = (192, 192, 192)
BLUE = (173, 216, 230)
TURQUOISE= (69,217,206)
YELLOW = (255, 255, 0)

# Sets up screen 
SCREEN = pg.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
SCREEN.fill(BLACK)

pg.display.set_caption("Network flows")

# Fonts
pg.font.init()
TITLEFONT = pg.font.SysFont("impact", 18)
FONT = pg.font.SysFont("arial", 12)
MEDIUMFONT = pg.font.SysFont("impact", 14)
SMALLFONT = pg.font.SysFont("arial", 10)
WRITINGFONT = pg.font.SysFont("consola", 14)
WRITINGFONTLETTERWIDTH = 7

# Padding for text within borders
SMALLPAD = 5
MEDIUMPAD = 20
LARGEPAD = 30

# 6 pixels = 0.1 on grid
GRIDLINEGAPS = 60

RADIUS = 30

EMPTYSTRING = " "

# Width for inputboxes and buttons
STRBUTTONWIDTH, INTBUTTONWIDTH = 40, 25
BUTTONHEIGHT = 20

# Edge height and widths
ARROWHEIGHT = 5
SMALLARROWWIDTH = 20
    
