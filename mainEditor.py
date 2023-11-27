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
        self.slowness = 0

class character:

    def __init__(self):

        self.speed = 50
        self.totalHealth = 100
        self.health = 100
        self.x = 0
        self.y = 0
        self.dx = 0
        self.dy = 0
        self.size = 10
        self.isMoving = False

        #direction
        self.moveToCoords = None
        self.moveToAngle = None

        self.targetCoords = None
        self.targetAngle = 0

        self.kills = 0

class lazers:

    def __init__(self):

        self.lazers = []
        self.dmg = 50
        self.color = "red"
        self.width = 2
        self.speed = 10
        self.cD = 50
        self.currentcD = 0

class icons:

    def __init__(self):

        self.x = None
        self.y = None
        self.timer = None

class upgradeBoxes:
        
    def __init__(self):
        self.rectWidth = None
        self.rectHeight = None
        self.gapWidth = None
        self.startX = None
        self.highlighted = None

class charUpgrades:

    def __init__(self):

        self.list = [False, False, False, False, False, False]
        self.Objects = []

        self.fourUpgrades = []

class freezingLazers(charUpgrades):
        
    def __init__(self):
        self.bossSpeedMultiplier = 1
        self.bossFreezeCD = 0

        self.setBossSpeedMultiplier = 0.5
        self.setBossFreezeCD = 60

        self.line1 = "lazers freeze"
        self.line2 = "the enemy"
        self.id = 0

    def activate(self, app):
        app.lazers1.color = "cyan"

class lazerDmg(charUpgrades):
        
    def __init__(self):
        self.line1 = "lazers do"
        self.line2 = "more damage"

        self.id = 1

    def activate(self, app):
        app.lazers1.dmg *= 1.2
        app.lazers1.width *= 1.2

class lazerAttackSpeed(charUpgrades):
        
    def __init__(self):

        self.line1 = "lazer cooldown"
        self.line2 = "is shorter"

        self.id = 2

    def activate(self, app):
        app.lazers1.cD *= 0.5

class fasterMS(charUpgrades):
        
    def __init__(self):
        self.speedMuliplier = 1.2

        self.line1 = "character moves"
        self.line2 = "faster"

        self.id = 3

    def activate(self, app):
        app.character1.speed *= 1.2

class increaseHP(charUpgrades):

    def __init__(self):
        self.line1 = "character gains"
        self.line2 = "double HP"

        self.id = 4

    def activate(self, app):
        app.character1.totalHealth *= 2
        app.character1.health *= 2

class dash(charUpgrades):

    def __init__(self):
        self.distance = 300

        self.line1 = "character gains a "
        self.line2 = "short dash ability"

        self.id = 5

        self.dx = None
        self.dy = None
        self.ready = False

        self.cD = 40
        self.curcD = 0

        self.isDashing = False

    def activate(self, app):
        pass
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

    app.boss1 = boss()
    app.character1 = character()
    app.lazers1 = lazers()
    app.map1 = map()

    #CHAR Upgrades
    if True:
        app.charUpgrades1 = charUpgrades()
        app.upgradeBoxes1 = upgradeBoxes()
        app.freezingLazers1 = freezingLazers()
        app.lazerDmg1 = lazerDmg()
        app.lazerAttackSpeed1 = lazerAttackSpeed()
        app.fasterMS1 = fasterMS()
        app.increaseHP1 = increaseHP()
        app.dash1 = dash()

        app.charUpgrades1.Objects = [app.freezingLazers1, app.lazerDmg1, app.lazerAttackSpeed1, app.fasterMS1, app.increaseHP1, app.dash1]
    
    app.boss1.respawnTimer = 1 #code to help testing


    app.stepPerSecond = 30
    app.time = 0
    
    app.situation = 0
    
    #CHAR VARIABLES
    if True:
        app.character1.x = app.width/2
        app.character1.y = app.gameHeight/2

    #sets the coordinates of the map
    app.map1.dx = app.character1.x
    app.map1.dy = app.character1.y

    #GIF

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
        app.spriteList = []
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
            app.spriteList.append(fr)
        app.spriteCounter = 0

    #char facing left
    if True:
        myGif = Image.open('images/kirb2.gif')
        app.spriteList2 = []
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
            app.spriteList2.append(fr)
        app.spriteCounter2 = 0

    #boss facing right
    if True:
        myGif = Image.open('images/kirb2.gif')
        app.spriteList3 = []
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
            app.spriteList3.append(fr)
        app.spriteCounter3 = 0

    #boss facing left
    if True:
        myGif = Image.open('images/kirb2.gif')
        app.spriteList4 = []
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
            app.spriteList4.append(fr)
        app.spriteCounter4 = 0

def resetBoss(app):
    app.boss1.x = 0
    app.boss1.y = 0
    app.boss1.health = app.boss1.totalHealth
    
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

    if app.character1.health:
        drawCharacter(app)

    if app.boss1.health:
        drawBoss(app)
        drawBossHealthbar(app)

    if app.lazers1.lazers:
        drawLasers(app)

    #game over screen
    if app.situation == 1:
        drawEnding1(app)

    #ugrade screen
    elif app.situation == 2:
        drawUpgradeSelector(app)

    #pause screen
    elif app.situation == 3:
        pauseScreen(app)
    
    drawBotBar(app)
    drawCharacterHealthbar(app)

#=======================================
#DRAWING HELPER FUNTIONS
#=======================================

#DRAWING MAP
def drawMap(app):
    
    drawRect(app.map1.dx, app.map1.dy, 7000, 7000, align = "center", fill = "lightblue")
    # drawPILImage takes in a PIL image object and the left-top coordinates
    drawImage(app.backround, app.map1.dx, app.map1.dy, align = "center")

#DRAWING Bottom Bar
def drawBotBar(app):
    drawRect(0, app.gameHeight, app.width, app.height - app.gameHeight, fill = 'black', opacity = 100)

#ENDING 1 SCREEN
def drawEnding1(app):
    drawRect(0, 0, app.width, app.height, fill = 'black', opacity = 40)
    drawLabel('GAME OVER', app.width/2, app.height/2-130, size = 40, bold = True, fill = "cyan")
    drawLabel(f'SCORE: {app.character1.kills}', app.width/2, app.height/2-70, size = 40, bold = True, fill = "cyan")
    drawLabel('PRESS L TO RESTART', app.width/2, app.height/2-10, size = 40, bold = True, fill = "cyan")

#PAUSE SCREEN
def pauseScreen(app):
    drawRect(0, 0, app.width, app.height, fill = 'black', opacity = 40)
    drawLabel('GAME IS PAUSED', app.width/2, app.height/2-100, size = 40, bold = True)

#DRAWS CHRACTER
def drawCharacter(app):

    if abs(app.character1.targetAngle) < math.pi/2:
        drawImage(app.spriteList[app.spriteCounter], app.character1.x, app.character1.y, align = 'center')
    else:
        drawImage(app.spriteList2[app.spriteCounter2], app.character1.x, app.character1.y, align = 'center')

#LAZERS   
def drawLasers(app):
    for lazer in app.lazers1.lazers:
        lazerXStart = lazer[0] - math.cos(lazer[2]) * 7
        lazerYStart = lazer[1] + math.sin(lazer[2]) * 7
        
        lazerXEnd = lazer[0] + math.cos(lazer[2]) * 7
        lazerYEnd = lazer[1] - math.sin(lazer[2]) * 7
        
        drawLine(lazerXStart, lazerYStart, lazerXEnd, lazerYEnd, fill = app.lazers1.color, lineWidth = app.lazers1.width)

#drawBoss
def drawBoss(app):
    if abs(app.boss1.targetAngle) < math.pi/2:
        drawImage(app.spriteList[app.spriteCounter], app.boss1.x, app.boss1.y, align = 'center')
    else:
        drawImage(app.spriteList2[app.spriteCounter2], app.boss1.x, app.boss1.y, align = 'center')
    
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

#character healthbar
def drawCharacterHealthbar(app):

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
    
#Uprgrade selector
def drawUpgradeSelector(app):

    rectWidth = app.width/5
    gapWidth = rectWidth/4
    rectHeight = app.height/1.5
    startX = app.width/2 - gapWidth * 1.5 - rectWidth * 1.5

    app.upgradeBoxes1.rectWidth = rectWidth
    app.upgradeBoxes1.rectHeight = rectHeight
    app.upgradeBoxes1.gapWidth = gapWidth
    app.upgradeBoxes1.startX = startX

    for i in range(4):

        x = startX + i * (gapWidth + rectWidth)

        if app.upgradeBoxes1.highlighted == i:
            drawRect(x, app.height/2, rectWidth+20, rectHeight+20, align = "center", fill = "cyan")
        drawRect(x, app.height/2, rectWidth, rectHeight, align = "center", fill = "white", border = "black")
        drawRect(x, app.height/2, rectWidth, rectHeight, align = "center", fill = "black", border = "black", opacity = 30)

        drawCharUpgrades(app, x, i)

def drawCharUpgrades(app, x, i):

    drawLabel(app.charUpgrades1.fourUpgrades[i].line1, x, app.height/2 - app.height*1/6, size = 25, bold = True)
    drawLabel(app.charUpgrades1.fourUpgrades[i].line2, x, app.height/2 - app.height*1/6 + 40, size = 25, bold = True)

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

def setMoveTo(app, mouseX, mouseY):

    app.character1.isMoving = True

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

def onMouseMove(app, mouseX, mouseY):

    if app.situation == 0:
        setTarget(app, mouseX, mouseY)
    elif app.situation == 2:
        checkIfHoverOverUpgrade(app, mouseX, mouseY)

def setTarget(app, mouseX, mouseY):
    #finds the angle that the mouse is facing
    #assigns the target coordinates of the mouse

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
        app.character1.targetAngle = math.asin(deltaY/hypotenuse)
    else:
        app.character1.targetAngle = math.pi - math.asin(deltaY/hypotenuse)

def checkIfHoverOverUpgrade(app, mouseX, mouseY):
    #returns the index of the box you are hovering over

    i = findBoxOfMouse(app, mouseX, mouseY)

    app.upgradeBoxes1.highlighted = i

def findBoxOfMouse(app, mouseX, mouseY):
    #returns the index of the box you are hovering over

    rectWidth = app.upgradeBoxes1.rectWidth
    rectHeight = app.upgradeBoxes1.rectHeight
    gapWidth = app.upgradeBoxes1.gapWidth
    startX = app.upgradeBoxes1.startX

    inBox = False
    for i in range(4):
        
        x = app.upgradeBoxes1.startX + i * (app.upgradeBoxes1.gapWidth + app.upgradeBoxes1.rectWidth)
        if inRect(app, x, app.height/2, app.upgradeBoxes1.rectHeight, app.upgradeBoxes1.rectWidth, mouseX, mouseY):
            return i
        
    return None

def pointInBounds(app, mouseX, mouseY):
    #makes sure the character is in bounds of the map
    #calculates the position of the chracter relative to the center of the backorund image
    #if the character is too far away in either direction, reset the coordinates to that of the bound

    deltaX = mouseX - app.character1.x
    deltaY = mouseY - app.character1.y

    targetX = deltaX - app.map1.dx
    targetY = deltaY - app.map1.dy

    rightBound = -app.width/2 + app.backroundWidth/2 - 100
    leftBound = -app.width/2 - app.backroundWidth/2 + 100
    bottomtBound = -app.gameHeight/2 + app.backroundHeight/2 - 100
    topBound = -app.gameHeight/2 - app.backroundHeight/2 + 100

    if targetX > rightBound:
        deltaX = rightBound + app.map1.dx
        mouseX = deltaX + app.character1.x
    elif targetX < leftBound:
        deltaX = leftBound + app.map1.dx
        mouseX = deltaX + app.character1.x
    if targetY > bottomtBound:
        deltaY = bottomtBound + app.map1.dy
        mouseY = deltaY + app.character1.y
    elif targetY < topBound:
        deltaY = topBound + app.map1.dy
        mouseY = deltaY + app.character1.y

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
        abilityCooldowns(app)

        if app.character1.isMoving:
            characterMove(app)
            moveMap(app)

        if len(app.lazers1.lazers) > 0:
            moveLazers(app)

        #SPAWNS BOSS AT TIME
        if app.boss1.health == 0:
            app.boss1.respawnTimer -= 1
            if app.boss1.respawnTimer == 0:
                resetBoss(app)

        if app.boss1.health:
            bossMove(app)

        #GIF
        animateChar(app)

        app.dash1.isDashing = False


#decreases ability cooldowns
def abilityCooldowns(app):

    if app.lazers1.currentcD > 0:
        app.lazers1.currentcD -= 1

    if app.freezingLazers1.bossFreezeCD > 0:
        app.freezingLazers1.bossFreezeCD -= 1

    if app.charUpgrades1.list[5] and app.dash1.curcD > 0:
        app.dash1.curcD -= 1

#finds the distance between where the chracter is moving to and the character and checks that it is higher then the chracter speed
def characterMove(app):

    #dash
    if app.dash1.ready and app.dash1.curcD <=0:

        app.character1.dx = app.dash1.dx
        app.character1.dy = app.dash1.dy

        app.character1.moveToCoords = [app.character1.x, app.character1.y]

        app.dash1.dx = 0
        app.dash1.dy = 0
        app.dash1.curcD = app.dash1.cD
        app.dash1.ready = False
        app.character1.isMoving = False
        app.dash1.isDashing = True

    else:
        #if greater then the speed the it sets the dx and dy values and decreases the moveTo Values
        if distance(app, app.character1.x, app.character1.y, app.character1.moveToCoords[0], app.character1.moveToCoords[1]) > app.character1.speed:

            app.character1.dx = (app.character1.speed * math.cos(app.character1.moveToAngle))
            app.character1.dy = -(app.character1.speed * math.sin(app.character1.moveToAngle))

            app.character1.moveToCoords[0] -= app.character1.dx
            app.character1.moveToCoords[1] -= app.character1.dy

        #else it sets move to coords to the coords of the character
        else:
            app.character1.moveToCoords[0], app.character1.moveToCoords[1] = app.character1.x, app.character1.y
            app.character1.isMoving = False

def moveMap(app):
    app.map1.dx -= app.character1.dx
    app.map1.dy -= app.character1.dy

#loops through all the lazers and moves them
#checks if any lazers collide with the boss and deals damage to the boss if so
def moveLazers(app):
    i = 0
    while i < len(app.lazers1.lazers):
        app.lazers1.lazers[i][0] = app.lazers1.lazers[i][0] + math.cos(app.lazers1.lazers[i][2]) * app.lazers1.speed
        app.lazers1.lazers[i][1] = app.lazers1.lazers[i][1] - math.sin(app.lazers1.lazers[i][2]) * app.lazers1.speed

        #frameshift lazers
        if app.character1.isMoving or app.dash1.isDashing:
            app.lazers1.lazers[i][0] -= app.character1.dx
            app.lazers1.lazers[i][1] -= app.character1.dy
        
        #if lazer hits boss
        if app.boss1.health and distance(app, app.boss1.x, app.boss1.y, app.lazers1.lazers[i][0], app.lazers1.lazers[i][1]) < app.boss1.size:
            #checks for freezin lazer
            if app.charUpgrades1.list[0]:
                app.freezingLazers1.bossSpeedMultiplier = app.freezingLazers1.setBossSpeedMultiplier
                app.freezingLazers1.bossFreezeCD = app.freezingLazers1.setBossFreezeCD 

            #does damage
            app.boss1.health -= app.lazers1.dmg
            app.lazers1.lazers.pop(i)
            checkBossDead(app)
        
        #delete lazer if out of bounds
        elif app.lazers1.lazers[i][0]>app.width or app.lazers1.lazers[i][0] < 0:
            app.lazers1.lazers.pop(i)
        elif app.lazers1.lazers[i][1]>app.gameHeight or app.lazers1.lazers[i][1] < 0:
            app.lazers1.lazers.pop(i)
        else:
            i+=1

#moves the boss towards the character onStep
def bossMove(app):
    
    if app.boss1.health:
    
        deltaY = (app.character1.y-app.boss1.y)
        deltaX = (app.character1.x-app.boss1.x) 
        hypotenuse = pythagoreanTheorem((app.character1.x-app.boss1.x), (app.character1.y-app.boss1.y))


        if deltaX >= 0:
            app.boss1.targetAngle = math.asin(deltaY/hypotenuse)
        else:
            app.boss1.targetAngle = math.pi - math.asin(deltaY/hypotenuse)
        
        bossXVelocity = deltaX/hypotenuse * app.boss1.speed
        bossYVelocity = -deltaY/hypotenuse * app.boss1.speed

        #freezing lasers
        if app.freezingLazers1.bossFreezeCD > 0:
            bossXVelocity *= app.freezingLazers1.bossSpeedMultiplier
            bossYVelocity *= app.freezingLazers1.bossSpeedMultiplier
        
        bossRightVelocity = bossXVelocity
        bossDownVelocity = -bossYVelocity
        
        app.boss1.x += bossRightVelocity
        app.boss1.y += bossDownVelocity

        #frameShift Boss
        if app.character1.isMoving or app.dash1.isDashing:
            app.boss1.x -= app.character1.dx
            app.boss1.y -= app.character1.dy
        
        bossAttack(app)

#checks if boss is in range to do a melee attack 
def bossAttack(app):
    if distance(app, app.boss1.x, app.boss1.y, app.character1.x, app.character1.y) < app.boss1.size:
        app.character1.health -= app.boss1.meleeDmg
        checkCharacterDead(app)

def checkCharacterDead(app):
    if app.character1.health <= 0:
        app.character1.health = 0
        app.situation = 1

def checkBossDead(app):
    if app.boss1.health <= 0:
        app.boss1.health = 0
        app.boss1.respawnTimer = 200   
        app.character1.kills += 1    

        #makes sure there are enough upgrades left
        if getNumUpgradesLeft(app):
            app.situation = 2
            get4Upgrades(app)

def get4Upgrades(app):
    #reset and generates the 4 upgrades that will be selected

    numberOfUpgrades = len(app.charUpgrades1.list)-1
    index = random.randint(1, numberOfUpgrades)
    usedIndexes = set()

    counter = 0
    while counter < 4:
        if app.charUpgrades1.list[index] == False and index not in usedIndexes:
            app.charUpgrades1.fourUpgrades.append(app.charUpgrades1.Objects[index])
            usedIndexes.add(index)
            counter+=1
        index = random.randint(0, numberOfUpgrades)

def getNumUpgradesLeft(app):

    counter = 0
    
    for i in range(len(app.charUpgrades1.list)):
        if app.charUpgrades1.list[i] == False:
            counter += 1

    if counter >= 4:
        return True
    return False

#GIF
def animateChar(app):
    #Set spriteCounter to next frame
    if app.time % 3 == 0:

        #char
        app.spriteCounter = (app.spriteCounter + 1) % len(app.spriteList)
        app.spriteCounter2 = (app.spriteCounter2 + 1) % len(app.spriteList2)

        #boss
        app.spriteCounter3 = (app.spriteCounter3 + 1) % len(app.spriteList3)
        app.spriteCounter4 = (app.spriteCounter4 + 1) % len(app.spriteList4)



    


#=======================================
#GENERAL HELPER FUNTIONS
#=======================================

def pythagoreanTheorem(x, y):
    return (x**2 + y**2)**0.5
    
def roundToThousands(app, num):
    return rounded(num*1000)/1000
    
def distance(app, x1, y1, x2, y2):
    return ((x2-x1)**2 + (y2-y1)**2)**0.5

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