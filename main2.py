from cmu_graphics import *
import math


#==============================================================================
#==============================================================================
#START
#==============================================================================
#==============================================================================

class map:

    def __init__(self):

        self.dx = 0
        self.dy = 0

class boss:

    def __init__(self):

        self.meleeDmg = 34
        self.totalHealth = 100
        self.health = 0
        self.speed = 1
        self.x = 0
        self.y = 0
        self.size = 40
        self.color = "purple"
        self.respawnTimer = 200

class character:

    def __init__(self):

        self.speed = 3
        self.totalHealth = 100
        self.health = 100
        self.x = 0
        self.y = 0
        self.dx = 0
        self.dy = 0
        self.size = 10

        #direction
        self.moveToCoords = None
        self.moveToAngle = None

        self.targetCoords = None
        self.targetAngle = None

        self.kills = 0

class lazers:

    def __init__(self):

        self.lazers = []
        self.dmg = 5
        self.color = "red"
        self.width = 1
        self.speed = 10
        self.cooldown = 0

class icons:

    def __init__(self):

        self.x = None
        self.y = None
        self.timer = None
        

#==============================================================================
#==============================================================================
#START
#==============================================================================
#==============================================================================
def onAppStart(app):
    
    #reize window
    app.width = 1400
    app.height = 900
    app.gameHeight = 800
    
    reset(app)
    
def reset(app):

    app.map1 = map()
    app.boss1 = boss()
    app.character1 = character()
    app.character1.x = app.width/2
    app.character1.y = app.gameHeight/2
    app.lazers1 = lazers()
    
    app.stepPerSecond = 30
    app.paused = True
    app.time = 0
    
    app.ending = 0

    
    #CHAR VARIABLES
    if True:
        app.character1.x = app.width/2
        app.character1.y = app.gameHeight/2
        
    #LAZERS
    app.lazers = []

# def resetBoss(app):
#     app.boss1.x = 0
#     app.boss1.y = 0
#     app.boss1.health = app.boss1.totalHealth
    
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
    drawBotBar(app)

    drawCharacterHealthBar(app)
    if app.character1.health:
        drawCharacter(app)

    if app.ending == 1:
        drawEnding1(app)

    else:
        if app.paused:
            pauseScreen(app)
    
#=======================================
#DRAWING HELPER FUNTIONS
#=======================================

#DRAWING MAP
def drawMap(app):
    drawRect(app.map1.dx + 0, app.map1.dy + 0, app.width, app.gameHeight, fill = 'black', opacity = 70)
    drawRect(app.map1.dx + 0, app.map1.dy + 300, app.width, 40, fill = 'black')
    drawRect(app.map1.dx + 0, app.map1.dy + 300, app.width, 40, fill = 'white', opacity = 50)
    drawRect(app.map1.dx + 400, app.map1.dy + 0, 40, app.gameHeight, fill = 'black')
    drawRect(app.map1.dx + 400, app.map1.dy + 0, 40, app.gameHeight, fill = 'white', opacity = 50)

#DRAWING Bottom Bar
def drawBotBar(app):
    drawRect(0, app.gameHeight, app.width, app.height - app.gameHeight, fill = 'black', opacity = 100)

#ENFING 1 SCREEN
def drawEnding1(app):
    drawRect(0, 0, app.width, app.height, fill = 'black', opacity = 40)
    drawLabel('GAME OVER', app.width/2, app.height/2-130, size = 40, bold = True, fill = "cyan")
    drawLabel(f'SCORE: {app.character1.kills}', app.width/2, app.height/2-70, size = 40, bold = True, fill = "cyan")

#PAUSE SCREEN
def pauseScreen(app):
    drawRect(0, 0, app.width, app.height, fill = 'black', opacity = 40)
    drawLabel('GAME IS PAUSED', app.width/2, app.height/2-100, size = 40, bold = True)

def drawCharacter(app):
    drawCircle(app.character1.x, app.character1.y, app.character1.size)


#character health bar
def drawCharacterHealthBar(app):

    healthBarSize = 500
    leftMargin = 40
    botMargin = 40
    border = 4
    
    drawRect(leftMargin+healthBarSize/2, app.height-botMargin, healthBarSize + border, 30 + border, align = 'center', border = 'black', borderWidth = 100)
    
    rectWidth = healthBarSize/app.character1.totalHealth
    startX = leftMargin + rectWidth/2
    
    for i in range(app.character1.totalHealth):
        
        if i < app.character1.health:
            color = 'green'
        elif i >= app.character1.health:
            color = rgb(200, 200, 200)
        
        drawRect(startX + i*rectWidth, app.height-botMargin, rectWidth, 30, align = 'center', fill = color)
        
    drawLabel(f'{app.character1.health} / {app.character1.totalHealth}', leftMargin+healthBarSize/2, app.height-botMargin, size = 20)
    

#==============================================================================
#==============================================================================
#CONTROLLERS
#==============================================================================
#==============================================================================
def onKeyPress(app, key):
    if key == 'p':
        app.paused = not(app.paused)


def onMousePress(app, mouseX, mouseY, button):
    
    if button == 2:
        setMoveTo(app, mouseX, mouseY)

def setMoveTo(app, mouseX, mouseY):

    app.character1.moveToCoords = [mouseX, mouseY]

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


#=======================================
#onStep
#=======================================     
def onStep(app):

    if app.paused:
        pass

    else:
        
        app.time += 1

        if app.character1.moveToCoords:
            characterMove(app)
            moveEverything(app)


def characterMove(app):

    #finds the distance between where the chracter is moving to and the character and checks that it is higher then the chracter speed
    #if greater then the speed the it sets the dx and dy values and decreases the moveTo Values
    #else it sets move to coords to the coords of the character
    if distance(app, app.character1.x, app.character1.y, app.character1.moveToCoords[0], app.character1.moveToCoords[1]) > app.character1.speed:

        app.character1.dx = (app.character1.speed * math.cos(app.character1.moveToAngle))
        app.character1.dy = -(app.character1.speed * math.sin(app.character1.moveToAngle))

        app.character1.moveToCoords[0] -= app.character1.dx
        app.character1.moveToCoords[1] -= app.character1.dy

    else:
        app.character1.moveToCoords[0], app.character1.moveToCoords[1] = app.character1.x, app.character1.y

def moveEverything(app):
    if distance(app, app.character1.x, app.character1.y, app.character1.moveToCoords[0], app.character1.moveToCoords[1]) != 0:
        app.map1.dx -= app.character1.dx
        app.map1.dy -= app.character1.dy



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