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
- game idea from Vampire Survivors
- framseshift got the idea of moving all the things on the screen from 2022 page
- Gif animation code from F23_demos 11/21 Lecture
- map backround code from F23_demos 11/21 Lecture
"""

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
        self.respawnTimer = 1
        self.slowness = 0
        self.targetAngle = 0

class lasers:

    def __init__(self):

        self.lasers = []
        self.dmg = 50
        self.color = "red"
        self.width = 2
        self.speed = 10
        self.cD = 50
        self.currentcD = 0

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
        app.targetDistance = None

        app.kills = 0

    #classes
    if True:
        app.boss1 = boss()
        app.lasers1 = lasers()


    #frameshift Variables
    if True:
        app.frameshiftX = 0
        app.frameshiftY = 0

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
            app.bossSpriteList1 = []
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
                app.bossSpriteList1.append(fr)
            app.bossSpriteCounter1 = 0

        #boss facing left
        if True:
            myGif = Image.open('images/kirb2.gif')
            app.bossSpriteList2 = []
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
                app.bossSpriteList2.append(fr)
            app.bossSpriteCounter2 = 0

def resetBoss(app):
    app.boss1.x = 0
    app.boss1.y = 0
    app.boss1.health = app.boss1.totalHealth
#==============================================================================
#==============================================================================
#DRAWING
#==============================================================================
#==============================================================================

def redrawAll(app):

    drawMap(app)

    if app.charHealth:
        drawCharacter(app)

    if app.boss1.health:
        drawBoss(app)
        drawBossHealthbar(app)

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
    
    drawRect(app.width/2-app.frameshiftX, app.gameHeight-app.frameshiftY, 7000, 7000, align = "center", fill = "lightblue")
    # drawPILImage takes in a PIL image object and the left-top coordinates
    drawImage(app.backround, app.width/2-app.frameshiftX, app.gameHeight/2-app.frameshiftY, align = "center")

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
    
#drawBoss
def drawBoss(app):

    x = app.boss1.x - app.frameshiftX
    y = app.boss1.y - app.frameshiftY

    print(x, y)

    if abs(app.boss1.targetAngle) < math.pi/2:
        drawImage(app.bossSpriteList1[app.bossSpriteCounter1], x , y, align = 'center')
    else:
        drawImage(app.bossSpriteList2[app.bossSpriteCounter2], x, y, align = 'center')
    
#boss healthbar
def drawBossHealthbar(app):

    healthBarSize = 800
    border = 4
    
    drawRect(app.width/2, 40, healthBarSize + border, 30 + border, align = 'center', border = 'black', borderWidth = 100)
    
    rectWidth = healthBarSize/app.boss1.totalHealth
    startX = app.width/2-healthBarSize/2+rectWidth/2
    
    for i in range(app.boss1.totalHealth):
        
        if i < app.boss1.health:
            color = 'red'
        elif i >= app.boss1.health:
            color = rgb(200, 200, 200)
        
        drawRect(startX + i*rectWidth, 40, rectWidth, 30, align = 'center', fill = color)
        
    drawLabel(f'{app.boss1.health} / {app.boss1.totalHealth}', app.width/2, 40, size = 20)

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

    elif app.situation == 1:
        if key == 'l':
            reset(app)

def stopMoving(app):
    app.moveToCoords = [app.width/2, app.gameHeight/2]
    app.charIsMoving = False

#==============================================================================
#onMousePress
#==============================================================================

def onMousePress(app, mouseX, mouseY, button):
    
    if app.situation == 0:
        if button == 2:
            setMoveTo(app, mouseX, mouseY)

    elif app.situation == 2:
        if button == 0:
            pass
            # selectUpgrade(app, mouseX, mouseY)

# sets - app.charIsMoving, app.moveToCoords, app.moveToAngle
def setMoveTo(app, mouseX, mouseY):

    app.charIsMoving = True
    app.moveToCoords = app.targetCoords
    app.moveToAngle = app.targetAngle
        
#==============================================================================
#Mouse Move
#==============================================================================  

def onMouseMove(app, mouseX, mouseY):

    if app.situation == 0:
        setTarget(app, mouseX, mouseY)
    elif app.situation == 2:
        pass
    
def setTarget(app, mouseX, mouseY):
    #finds the angle that the mouse is facing
    #assigns the target coordinates of the mouse
    #sets app.targetCoords, app.targetDistance, app.character1.targetAngle

    #makes sure the point is in bounds
    res = pointInBounds(app, mouseX, mouseY)
    app.targetCoords = res[1]
    deltaX = res[0][0]
    deltaY = res[0][1]

    hypotenuse = pythagoreanTheorem(deltaX, deltaY)

    app.targetDistance = hypotenuse

    #make sure no crash
    if hypotenuse == 0:
        pass
    elif deltaX >= 0:
        app.targetAngle = math.asin(deltaY/hypotenuse)
    else:
        app.targetAngle = math.pi - math.asin(deltaY/hypotenuse)

def pointInBounds(app, mouseX, mouseY):
    #makes sure the character is in bounds of the map
    #calculates the position of the chracter relative to the center of the backorund image
    #if the character is too far away in either direction, reset the coordinates to that of the bound

    deltaX = mouseX - app.charX
    deltaY = mouseY - app.charY

    deltaY = -deltaY

    return [[deltaX, deltaY], [mouseX, mouseY]]
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

        #SPAWNS BOSS AT TIME
        if app.boss1.health == 0:
            app.boss1.respawnTimer -= 1
            if app.boss1.respawnTimer == 0:
                resetBoss(app)

        if app.boss1.health:
            bossMove(app)

        #GIF
        animateChar(app)

#finds the distance between where the chracter is moving to and the character and checks that it is higher then the chracter speed
def characterMove(app):

    #if greater then the speed the it sets the dx and dy values and decreases the moveTo Values
    if distance(app, app.charX, app.charY, app.moveToCoords[0], app.moveToCoords[1]) > app.charSpeed:

        graphicsHorizontalMovement = app.charSpeed * math.cos(app.moveToAngle)
        graphicsVerticalMovement = -(app.charSpeed * math.sin(app.moveToAngle))

        app.frameshiftX += graphicsHorizontalMovement
        app.frameshiftY += graphicsVerticalMovement

        app.moveToCoords[0] -= graphicsHorizontalMovement
        app.moveToCoords[1] -= graphicsVerticalMovement

    #else it sets move to coords to the coords of the character
    else:
        app.moveToCoords[0], app.moveToCoords[1] = app.charX, app.charY
        app.charIsMoving = False

#GIF
def animateChar(app):
    #Set spriteCounter to next frame
    if app.time % 3 == 0:

        #char
        app.charSpriteCounter1 = (app.charSpriteCounter1 + 1) % len(app.charSpriteList1)
        app.charSpriteCounter2 = (app.charSpriteCounter2 + 1) % len(app.charSpriteList2)

        #boss
        app.bossSpriteCounter1 = (app.bossSpriteCounter1 + 1) % len(app.bossSpriteList1)
        app.bossSpriteCounter2 = (app.bossSpriteCounter2 + 1) % len(app.bossSpriteList2)

#moves the boss towards the character onStep
def bossMove(app):
    
    if app.boss1.health:

        x = app.boss1.x - app.frameshiftX
        y = app.boss1.y - app.frameshiftY
    
        deltaX = (app.charX-x)
        deltaY = (app.charY-y)

        deltaY = -deltaY 

        hypotenuse = pythagoreanTheorem(deltaX, deltaY)
        
        #make sure no crash
        if hypotenuse == 0:
            pass
        else:
            if deltaX >= 0:
                app.boss1.targetAngle = math.asin(deltaY/hypotenuse)
            else:
                app.boss1.targetAngle = math.pi - math.asin(deltaY/hypotenuse)
            
            graphicsHorizontalMovement = deltaX/hypotenuse * app.boss1.speed
            graphicsVerticalMovement = -(deltaY/hypotenuse * app.boss1.speed)

            #frameShift Boss
            app.boss1.x += graphicsHorizontalMovement
            app.boss1.y += graphicsVerticalMovement
            
            bossAttack(app)

#checks if boss is in range to do a melee attack 
def bossAttack(app):

    bossX = app.boss1.x - app.frameshiftX
    bossY = app.boss1.y - app.frameshiftY

    if distance(app, bossX, bossY, app.charX, app.charY) < app.boss1.size:
        app.charHealth -= app.boss1.meleeDmg
        checkCharacterDead(app)

def checkCharacterDead(app):
    if app.charHealth <= 0:
        app.charHealth = 0
        app.situation = 1

def checkBossDead(app):
    if app.boss1.health <= 0:
        app.boss1.health = 0
        app.boss1.respawnTimer = 200   
        app.kills += 1    

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




















































