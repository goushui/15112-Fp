from cmu_graphics import *
import math


#==============================================================================
#==============================================================================
#START
#==============================================================================
#==============================================================================

class boss:

    def __init__(self):

        self.speed = 10
        self.health = 100

class character:

    def __init__(self):

        self.speed = 3
        self.health = 100
        self.x = 0
        self.y = 0
        self.size = 10

        #direction
        self.moveToCoords = None
        self.moveToAngle = None

        self.targetCoords = None
        self.targetAngle = None

class lazers:

    def __init__(self):

        self.lazers = []

#==============================================================================
#==============================================================================
#START
#==============================================================================
#==============================================================================
def onAppStart(app):

    app.boss1 = boss()
    app.character1 = character()
    app.lazers1 = lazers()
    
    #reize window
    app.width = 1400
    app.height = 900
    
    reset(app)
    
def reset(app):
    
    app.stepPerSecond = 30
    app.paused = True
    app.time = 0
    
    #DISPLAY
    app.displaySpeed = 0
    app.displayDegees = 0
    app.displayTime = 0
    
    #Player Variables
    app.dead = False
    
    #CHAR VARIABLES
    if True:
        app.character1.x = app.width/2
        app.character1.y = app.height/2
        
        #LAZERS
        app.lazers = []
    
    app.isBoss = False
    
#=======================================
#MODEL HELPER FUNTIONS
#=======================================


#==============================================================================
#==============================================================================
#DRAWING
#==============================================================================
#==============================================================================
def redrawAll(app):

    drawMap(app)

    if app.paused:
        pauseScreen(app)

    if app.character1.health:
        drawCharacter(app)
    
#=======================================
#DRAWING HELPER FUNTIONS
#=======================================

#DRAWING MAP
def drawMap(app):
    drawRect(0, 0, app.width, app.height, fill = 'Green', opacity = 90)
    drawRect(0, 300, app.width, 40, fill = 'black')
    drawRect(0, 300, app.width, 40, fill = 'white', opacity = 50)
    drawRect(400, 0, 40, app.height, fill = 'black')
    drawRect(400, 0, 40, app.height, fill = 'white', opacity = 50)

#PAUSE SCREEN
def pauseScreen(app):
    drawRect(0, 0, app.width, app.height, fill = 'black', opacity = 40)
    drawLabel('GAME IS PAUSED', app.width/2, app.height/2-100, size = 40, bold = True)

def drawCharacter(app):
    drawCircle(app.character1.x, app.character1.y, app.character1.size)
    

#==============================================================================
#==============================================================================
#CONTROLLERS
#==============================================================================
#==============================================================================
def onKeyPress(app, key):
    if key == 'p':
        app.paused = not(app.paused)

    #lazers
    if key == 'q':
        app.lazers1.lazers.append([app.character1.x, app.character1.y, app.character1.targetAngle])


def onMousePress(app, mouseX, mouseY):

    movement(app, mouseX, mouseY)

def movement(app, mouseX, mouseY):

    app.character1.moveToCoords = mouseX, mouseY

    deltaX = mouseX - app.character1.x
    deltaY = -(mouseY - app.character1.y)

    hypotenuse = pythagoreanTheorem(deltaX, deltaY)
    
    if deltaX >= 0:
        app.character1.moveToAngle = math.asin(deltaY/hypotenuse)

    else:
        app.character1.moveToAngle = math.pi - math.asin(deltaY/hypotenuse)
        
#=======================================
#Mouse Move
#=======================================  

def onMouseMove(app, mouseX, mouseY):

    app.targetCoords = mouseX, mouseY

    deltaX = mouseX - app.character1.x
    deltaY = -(mouseY - app.character1.y)

    hypotenuse = pythagoreanTheorem(deltaX, deltaY)
    
    if deltaX >= 0:
        app.character1.targetAngle = math.asin(deltaY/hypotenuse)

    else:
        app.character1.targetAngle = math.pi - math.asin(deltaY/hypotenuse)

#def onKeyHold(app, keys):

        
# def onKeyRelease(app, key):
    

#=======================================
#onStep
#=======================================     
def onStep(app):

    if app.paused:
        pass

    else:

        if app.character1.moveToCoords:
            moveCharacter(app)

def moveCharacter(app):

    x, y = app.character1.moveToCoords

    if distance(app, app.character1.x, app.character1.y, x, y) > app.character1.speed:

        app.character1.x += (app.character1.speed * math.cos(app.character1.moveToAngle))
        app.character1.y += -(app.character1.speed * math.sin(app.character1.moveToAngle))
    else:
        app.character1.x = x
        app.character1.y = y

#=======================================
#GENERAL HELPER FUNTIONS
#=======================================

def pythagoreanTheorem(x, y):
    return (x**2 + y**2)**0.5
    
def roundToThousands(app, num):
    return rounded(num*1000)/1000
    
def distance(app, x1, y1, x2, y2):
    return ((x2-x1)**2 + (y2-y1)**2)**0.5


#=======================================
#MAIN
#=======================================
def main():
    runApp()

main()