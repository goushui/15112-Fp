from cmu_graphics import *
from PIL import Image
import os, pathlib
import math
import random


"""
Why is my game laggy?
are my comments okay?

to do
-make randomly generted map
    rocks
-make sprites
-make pathfinding
-add images for the upgrades



citations:
- framseshift got the idea of moving all the things on the screen from 2022 page
- Gif animation code from F23_demos 11/21 Lecture
- map backround code from F23_demos 11/21 Lecture
"""


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
    
#resets the game
def reset(app):

    #game Variables
    if True:
        app.time = 0
        app.situation = 0

    #character variables
    if True:
        app.charSpeed = 3
        app.charTotalHealth = 100
        app.charHealth = 100
        app.charX = app.width/2
        app.charY = app.gameHeight/2
        app.size = 10
        app.charIsMoving = False

        #direction
        app.moveToCoords = None
        app.moveToAngle = None

        app.targetCoords = None
        app.targetAngle = 0

        app.kills = 0

    #frameshift Variables
    if True:
        app.frameShiftX = app.width/2
        app.frameShiftY = app.gameHeight/2

    #Images====================================================================
    if True:
        #map
        if True:
            # Open image from local directory
            app.backround = Image.open('images/grass.gif')

            #makes the size of the backround
            app.backroundWidth = 5000
            app.backroundHeight = 5000
            app.backround = app.backround.resize((app.backroundWidth, app.backroundHeight))

            # Cast image type to CMUImage to allow for faster drawing
            app.backround = CMUImage(app.backround)

        #char facing right
        if True:

            myGif = Image.open('images/kirb.gif')
            app.charSpriteList1 = []
            for frame in range(myGif.n_frames):
                #Set the current frame
                myGif.seek(frame)
                #Resize the image
                fr = myGif.resize((myGif.size[0]//2, myGif.size[1]//2))
                #Flip the image
                fr = fr.transpose(Image.FLIP_LEFT_RIGHT)
                #Convert to CMUImage
                fr = CMUImage(fr)
                #Put in our sprite list
                app.charSpriteList1.append(fr)
            app.charSpriteCounter1 = 0

        #char facing left
        if True:
            myGif = Image.open('images/kirb2.gif')
            app.charSpriteList2 = []
            for frame in range(myGif.n_frames):
                #Set the current frame
                myGif.seek(frame)
                #Resize the image
                fr = myGif.resize((myGif.size[0]//2, myGif.size[1]//2))
                #Flip the image
                fr = fr.transpose(Image.FLIP_LEFT_RIGHT)
                #Convert to CMUImage
                fr = CMUImage(fr)
                #Put in our sprite list
                app.charSpriteList2.append(fr)
            app.charSpriteCounter2 = 0

        #boss facing right
        if True:
            myGif = Image.open('images/kirb2.gif')
            app.charSpriteList3 = []
            for frame in range(myGif.n_frames):
                #Set the current frame
                myGif.seek(frame)
                #Resize the image
                fr = myGif.resize((myGif.size[0]//2, myGif.size[1]//2))
                #Flip the image
                fr = fr.transpose(Image.FLIP_LEFT_RIGHT)
                #Convert to CMUImage
                fr = CMUImage(fr)
                #Put in our sprite list
                app.charSpriteList3.append(fr)
            app.charSpriteCounter3 = 0

        #boss facing left
        if True:
            myGif = Image.open('images/kirb2.gif')
            app.charSpriteList4 = []
            for frame in range(myGif.n_frames):
                #Set the current frame
                myGif.seek(frame)
                #Resize the image
                fr = myGif.resize((myGif.size[0]//2, myGif.size[1]//2))
                #Flip the image
                fr = fr.transpose(Image.FLIP_LEFT_RIGHT)
                #Convert to CMUImage
                fr = CMUImage(fr)
                #Put in our sprite list
                app.charSpriteList4.append(fr)
            app.charSpriteCounter4 = 0

#==============================================================================
#==============================================================================
#DRAWING
#==============================================================================
#==============================================================================

def redrawAll(app):

    drawMap(app)

    if app.charHealth:
        drawCharacter(app)

    #game over screen
    if app.situation == 1:
        drawEnding1(app)

    #pause screen
    elif app.situation == 3:
        pauseScreen(app)
    
    drawBotBar(app)
    drawCharacterHealthbar(app)

#==========================================================================
#DRAWING HELPER FUNTIONS
#==========================================================================


#DRAWING MAP
def drawMap(app):
    
    drawRect(app.frameShiftX, app.frameShiftY, 7000, 7000, align = "center", fill = "lightblue")
    # drawPILImage takes in a PIL image object and the left-top coordinates
    drawImage(app.backround, app.frameShiftX, app.frameShiftY, align = "center")

#DRAWING Bottom Bar
def drawBotBar(app):
    drawRect(0, app.gameHeight, app.width, app.height - app.gameHeight, fill = 'black', opacity = 100)

#ENDING 1 SCREEN
def drawEnding1(app):
    drawRect(0, 0, app.width, app.height, fill = 'black', opacity = 40)
    drawLabel('GAME OVER', app.width/2, app.height/2-130, size = 40, bold = True, fill = "cyan")
    drawLabel(f'SCORE: {app.kills}', app.width/2, app.height/2-70, size = 40, bold = True, fill = "cyan")
    drawLabel('PRESS L TO RESTART', app.width/2, app.height/2-10, size = 40, bold = True, fill = "cyan")

#PAUSE SCREEN
def pauseScreen(app):
    drawRect(0, 0, app.width, app.height, fill = 'black', opacity = 40)
    drawLabel('GAME IS PAUSED', app.width/2, app.height/2-100, size = 40, bold = True)

#DRAWS CHRACTER
def drawCharacter(app):

    if abs(app.targetAngle) < math.pi/2:
        drawImage(app.charSpriteList1[app.charSpriteCounter1], app.charX, app.charY, align = 'center')
    else:
        drawImage(app.charSpriteList2[app.charSpriteCounter2], app.charX, app.charY, align = 'center')

#character healthbar
def drawCharacterHealthbar(app):

    healthBarSize = 500
    leftMargin = 40
    botMargin = 40
    border = 4
    
    drawRect(leftMargin+healthBarSize/2, app.height-botMargin, healthBarSize + border, 30 + border, align = 'center', border = 'black', borderWidth = 100)
    
    rectWidth = healthBarSize/app.charTotalHealth
    startX = leftMargin + rectWidth/2
    
    for i in range(app.charTotalHealth):
        
        if i < app.charHealth:
            color = 'green'
        elif i >= app.charHealth:
            color = rgb(200, 200, 200)
        
        drawRect(startX + i*rectWidth, app.height-botMargin, rectWidth, 30, align = 'center', fill = color)
        
    drawLabel(f'{app.charHealth} / {app.charTotalHealth}', leftMargin+healthBarSize/2, app.height-botMargin, size = 20)
    
#==============================================================================
#==============================================================================
#CONTROLLERS
#==============================================================================
#==============================================================================

#==============================================================================
#onKeyPress
#==============================================================================
def onKeyPress(app, key):
    if app.situation == 0:
        if key == 'p':
            if app.situation == 0:
                app.situation = 3
            elif app.situation == 3:
                app.situation = 0

        elif key == 's':
            stopMoving(app)
        #lazers
        elif key == 'q' and app.lazers1.currentcD == 0:
            app.lazers1.currentcD = app.lazers1.cD
            app.lazers1.lazers.append([app.character1.x, app.character1.y, app.character1.targetAngle])

        #dash
        elif key == 'e' and app.charUpgrades1.list[5] and app.dash1.curcD <= 0:
            dashes(app)
    elif app.situation == 1:
        if key == 'l':
            reset(app)

def dashes(app):

    dashDistance = min(app.targetDistance, app.dash1.distance)
    
    #changes dx base on the length of the dash and the position of the mouse
    app.dash1.dx = (dashDistance * math.cos(app.character1.targetAngle))
    app.dash1.dy = -(dashDistance * math.sin(app.character1.targetAngle))
    app.dash1.ready = True
    app.character1.isMoving = True

def stopMoving(app):
    app.character1.moveToCoords = [app.width/2, app.gameHeight/2]
    app.character1.isMoving = False

#==============================================================================
#onMousePress
#==============================================================================

def onMousePress(app, mouseX, mouseY, button):
    
    if app.situation == 0:
        if button == 2:
            setMoveTo(app, mouseX, mouseY)

    elif app.situation == 2:
        if button == 0:
            selectUpgrade(app, mouseX, mouseY)

def selectUpgrade(app, mouseX, mouseY):
    #finds if the chracter click in a box
    #takes the id of the upgrade the character clicked on and turns it on
    #resets the situation to 0
    #resets the four upgrades

    i = findBoxOfMouse(app, mouseX, mouseY)

    if i != None:
        upgrd = app.charUpgrades1.fourUpgrades[i]
        upgrd.activate(app)
        id = upgrd.id
        app.charUpgrades1.list[id] = True
        app.situation = 0
        app.charUpgrades1.fourUpgrades = []


"""
sets a point to where the chracter is moving
sets 
 - app.charIsMoving = True
 - app.moveToCoords

"""
def setMoveTo(app, mouseX, mouseY):

    app.charIsMoving = True

    #makes sure the point is in bounds
    res = pointInBounds(app, mouseX, mouseY)
    app.character1.moveToCoords = res[1]
    deltaX = res[0][0]
    deltaY = res[0][1]

    hypotenuse = pythagoreanTheorem(deltaX, deltaY)

    #make sure no crash
    if hypotenuse == 0:
        pass
    elif deltaX >= 0:
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

    if app.situation == 1:
        pass
    elif app.situation == 2:
        pass
    elif app.situation == 3:
        pass
    else:
        app.time += 1

        if app.charIsMoving:
            characterMove(app)
            moveMap(app)

        #GIF
        animateChar(app)

#finds the distance between where the chracter is moving to and the character and checks that it is higher then the chracter speed
def characterMove(app):

    #if greater then the speed the it sets the dx and dy values and decreases the moveTo Values
    if distance(app, app.character1.x, app.character1.y, app.character1.moveToCoords[0], app.character1.moveToCoords[1]) > app.character1.speed:

        app.character1.dx += (app.character1.speed * math.cos(app.character1.moveToAngle))
        app.character1.dy -= (app.character1.speed * math.sin(app.character1.moveToAngle))

        app.character1.moveToCoords[0] = app.character1.dx
        app.character1.moveToCoords[1] = app.character1.dy

    #else it sets move to coords to the coords of the character
    else:
        app.character1.moveToCoords[0], app.character1.moveToCoords[1] = app.character1.x, app.character1.y
        app.character1.isMoving = False

def moveMap(app):
    app.map1.dx -= app.character1.dx
    app.map1.dy -= app.character1.dy


#GIF
def animateChar(app):
    #Set spriteCounter to next frame
    if app.time % 3 == 0:

        #char
        app.charSpriteCounter1 = (app.charSpriteCounter1 + 1) % len(app.charSpriteList1)
        app.charSpriteCounter2 = (app.charSpriteCounter2 + 1) % len(app.charSpriteList2)

        #boss
        app.charSpriteCounter3 = (app.charSpriteCounter3 + 1) % len(app.charSpriteList3)
        app.charSpriteCounter4 = (app.charSpriteCounter4 + 1) % len(app.charSpriteList4)


#=======================================
#GENERAL HELPER FUNTIONS
#=======================================

def pythagoreanTheorem(x, y):
    return (x**2 + y**2)**0.5
    
def roundToThousands(app, num):
    return rounded(num*1000)/1000
    
def distance(app, x1, y1, x2, y2):
    return ((x2-x1)**2 + (y2-y1)**2)**0.5

#checks if a set of coordinates are inside a rectangle
def inRect(app, centerX, centerY, height, width, pointerX, pointerY):
    leftBound = centerX - width/2
    rightBound = centerX + width/2
    topBound = centerY - height/2
    botBound = centerY + height/2

    if leftBound < pointerX < rightBound and topBound < pointerY < botBound:
        return True
    return False

#=======================================
#MAIN
#=======================================
def main():
    runApp()

main()




















































