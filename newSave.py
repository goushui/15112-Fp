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
-make sprites
-make pathfinding
-add images for the upgrades



Citations:
- game idea from Vampire Survivors
- framseshift got the idea of moving all the things on the screen from 2022 page
- Gif animation code from F23_demos 11/21 Lecture
- map backround code from F23_demos 11/21 Lecture
- pathfinding algorithm from https://www.youtube.com/watch?v=-L-WgKMFuhE&t=405s
"""

class boss:

    def __init__(self):

        self.meleeDmg = 34
        self.totalHealth = 100
        self.health = 0
        self.speed = 2
        self.x = 0
        self.y = 0
        self.lastX = 0
        self.lastY = 0
        self.size = 30
        self.color = "purple"
        self.respawnTimer = 1
        self.slowness = 0
        self.targetAngle = 0
        self.isMoving = False

        self.targetX = 0
        self.targetY = 0

        self.targetGridX = 0
        self.targetGridY = 0

    def reset(self):

        self.health = self.totalHealth

        self.isMoving = False

        self.targetX = 0
        self.targetY = 0

        self.targetGridX = 0
        self.targetGridY = 0

class lasers:

    def __init__(self):

        self.lasers = []
        self.dmg = 50
        self.color = "red"
        self.width = 2
        self.speed = 10
        self.setCD = 50
        self.currentCD = 0

class Node:

    def __init__(self, x, y):
        #grid values
        self.x = x
        self.y = y

        self.gCost = 0
        self.hCost = 0
        self.fCost = 0

        self.traversable = True

        self.parent = None

        self.baseColor = "lightgreen"
        self.color = "lightgreen"

    def clacFCost(self):
        self.fCost = self.gCost + self.hCost

    def __eq__(self, other):

        return isinstance(other, Node) and self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f"{(self.x, self.y)}"

class upgradeBoxes:
        
    def __init__(self):
        self.rectWidth = None
        self.rectHeight = None
        self.gapWidth = None
        self.startX = None
        self.highlighted = None

class charUpgrades:

    def __init__(self):

        self.list = [False, False, False, False, False]
        self.Objects = []

        self.fourUpgrades = []

class freezingLazers(charUpgrades):
        
    def __init__(self):
        self.bossSpeedMultiplier = 1
        self.bossFreezeCD = 0

        self.setBossSpeedMultiplier = 0
        self.setBossFreezeCD = 60

        self.line1 = "lazers freeze"
        self.line2 = "the enemy"
        self.id = 0

    def activate(self, app):
        app.lasers1.color = "cyan"

class lazerDmg(charUpgrades):
        
    def __init__(self):
        self.line1 = "lazers do"
        self.line2 = "more damage"

        self.id = 1

    def activate(self, app):
        app.lasers1.dmg *= 1.2
        app.lasers1.width *= 1.2

class lazerAttackSpeed(charUpgrades):
        
    def __init__(self):

        self.line1 = "lazer cooldown"
        self.line2 = "is shorter"

        self.id = 2

    def activate(self, app):
        app.lasers1.setCD *= 0.1

class fasterMS(charUpgrades):
        
    def __init__(self):
        self.speedMuliplier = 2

        self.line1 = "character moves"
        self.line2 = "faster"

        self.id = 3

    def activate(self, app):
        app.charSpeed *= 4

class increaseHP(charUpgrades):

    def __init__(self):
        self.line1 = "character gains"
        self.line2 = "double HP"

        self.id = 4

    def activate(self, app):
        app.charTotalHealth *= 2
        app.charHealth *= 2

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
        app.charSize = 30
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

    generateImagesAndGifs(app)

    #frameshift Variables
    if True:
        app.frameshiftX = 0
        app.frameshiftY = 0

        app.lastFrameshiftX = 0
        app.lastFrameshiftY = 0

    #grid
    if True:
        generateGrid(app)
        generateWalls(app)

        #CHAR Upgrades
    
    #creates character upgrade objects
    if True:
        app.charUpgrades1 = charUpgrades()
        app.upgradeBoxes1 = upgradeBoxes()
        app.freezingLazers1 = freezingLazers()
        app.lazerDmg1 = lazerDmg()
        app.lazerAttackSpeed1 = lazerAttackSpeed()
        app.fasterMS1 = fasterMS()
        app.increaseHP1 = increaseHP()

        app.charUpgrades1.Objects = [app.freezingLazers1, app.lazerDmg1, app.lazerAttackSpeed1, app.fasterMS1, app.increaseHP1]
    
#resets the boss
def resetBoss(app):

    app.boss1.reset()

    randBossSpawn(app)

    app.boss1.health = app.boss1.totalHealth

    #Node
    app.bossNode = None
    app.bossPath = []

def generateImagesAndGifs(app):

    #map
    if True:
        # Open image from local directory
        app.backround = Image.open('images/grass.gif')

        #makes the size of the backround
        app.backroundWidth = 1000
        app.backroundHeight = 1000
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

        myGif = Image.open('images/kirb.gif')
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

#sets the starting coordinates of the boss to a random corner grid
def randBossSpawn(app):

    i = random.randint(1, 4)
    if i == 1:
        app.boss1.x = app.width/2 - app.backroundWidth/2 + app.nodeWidth*3/2
        app.boss1.y = app.gameHeight/2 - app.backroundHeight/2 + app.nodeHeight*3/2
    elif i==2:
        app.boss1.x = app.width/2 - app.backroundWidth/2 + app.nodeWidth*3/2
        app.boss1.y = app.gameHeight/2 + app.backroundHeight/2 - app.nodeHeight*3/2
    elif i==3:
        app.boss1.x = app.width/2 + app.backroundWidth/2 - app.nodeWidth*3/2
        app.boss1.y = app.gameHeight/2 - app.backroundHeight/2 + app.nodeHeight*3/2
    elif i==4:
        app.boss1.x = app.width/2 + app.backroundWidth/2 - app.nodeWidth*3/2
        app.boss1.y = app.gameHeight/2 + app.backroundHeight/2 - app.nodeHeight*3/2

#==============================================================================
#==============================================================================
#DRAWING
#==============================================================================
#==============================================================================

def redrawAll(app):

    drawMap(app)

    drawGrid(app)

    if app.charHealth:
        drawCharacter(app)

    if app.boss1.health:
        drawBoss(app)
        drawBossHealthbar(app)
        drawPointerTarget(app)

    if app.lasers1.lasers:
        drawLasers(app)

    #game over screen
    if app.situation == 1:
        drawEnding1(app)

    #characterUpgrades
    elif app.situation == 2:
        drawUpgradeSelector(app)

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
    
    drawRect(app.width/2-app.frameshiftX, app.gameHeight/2-app.frameshiftY, app.backroundWidth+1000, app.backroundHeight+1000, align = "center", fill = "lightblue")
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

def drawPointerTarget(app):
    drawCircle(app.boss1.targetX, app.boss1.targetY, 5, fill = "red")

#LASERS   
def drawLasers(app):
    for laser in app.lasers1.lasers:
        #creates start and end points for the lasets
        laserXStart = laser[0] - math.cos(laser[2]) * 7
        laserYStart = laser[1] + math.sin(laser[2]) * 7
        
        laserXEnd = laser[0] + math.cos(laser[2]) * 7
        laserYEnd = laser[1] - math.sin(laser[2]) * 7
        
        drawLine(laserXStart - app.frameshiftX, laserYStart - app.frameshiftY, laserXEnd - app.frameshiftX, laserYEnd - app.frameshiftY, fill = app.lasers1.color, lineWidth = app.lasers1.width)

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
        elif key == 'q' and app.lasers1.currentCD == 0:
            app.lasers1.currentCD = app.lasers1.setCD
            app.lasers1.lasers.append([app.charX + app.frameshiftX, app.charY + app.frameshiftY, app.targetAngle, 0])


    elif app.situation == 1:
        if key == 'l':
            reset(app)

#stops the chracter form moving
def stopMoving(app):
    app.moveToCoords = [app.width/2, app.gameHeight/2]
    app.charIsMoving = False

#==============================================================================
#onMousePress
#==============================================================================

def onMousePress(app, mouseX, mouseY, button):
    
    if app.situation == 0:
        if button == 2:
            col, row = findTargetNode(app, app.targetCoords[0], app.targetCoords[1])
            setTargetNode(app, col, row)
            if checkCanRightClick(app, row, col) == False:
                if app.charNode == app.targetNode:
                    setMoveTo(app)
                else:
                    app.charPath = pathfinding(app, app.charNode, app.targetNode)

    #characterUpgrades
    elif app.situation == 2:
        if button == 0:
            selectUpgrade(app, mouseX, mouseY)

# sets - app.charIsMoving, app.moveToCoords, app.moveToAngle
def setMoveTo(app):

    app.charIsMoving = True
    app.moveToCoords = app.targetCoords
    app.moveToAngle = app.targetAngle
        
#==============================================================================
#Mouse Move
#==============================================================================  

def onMouseMove(app, mouseX, mouseY):

    if app.situation == 0:
        setTarget(app, mouseX, mouseY)
    #characterUpgrades
    elif app.situation == 2:
        checkIfHoverOverUpgrade(app, mouseX, mouseY)
    
def setTarget(app, mouseX, mouseY):
    #finds the angle that the mouse is facing
    #assigns the target coordinates of the mouse
    #sets app.targetCoords, app.targetDistance, app.character1.targetAngle

    #makes sure the point is in bounds

    deltaX = mouseX - app.charX
    deltaY = mouseY - app.charY

    deltaY = -deltaY

    app.targetCoords = [mouseX, mouseY]

    hypotenuse = pythagoreanTheorem(deltaX, deltaY)

    app.targetDistance = hypotenuse

    #make sure no crash
    if hypotenuse == 0:
        pass
    elif deltaX >= 0:
        app.targetAngle = math.asin(deltaY/hypotenuse)
    else:
        app.targetAngle = math.pi - math.asin(deltaY/hypotenuse)

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

        if app.charIsMoving:
            characterMove(app)
        elif app.charPath and len(app.charPath) > 0:
            pathfindingMovement(app)

        #SPAWNS BOSS AT TIME
        if app.boss1.health == 0:
            app.boss1.respawnTimer -= 1
            if app.boss1.respawnTimer == 0:
                resetBoss(app)

        #nodes
        findCharNode(app)

        if app.boss1.health:
            findBossNode(app)
            if app.boss1.isMoving == False:
                app.boss1.isMoving = True
                app.bossPath = pathfinding(app, app.bossNode, app.charNode)
                if len(app.bossPath) > 0:
                    setBossPathfindingMovement(app)
            else:
                bossPathfindingMovement(app)

            findBossNode(app)

        if len(app.lasers1.lasers) > 0:
            moveLasers(app)

        findCharNode(app)

        #GIF
        animateChar(app)

        #updates last coordinates if collision
        app.lastFrameshiftX = app.frameshiftX
        app.lastFrameshiftY = app.frameshiftY

        app.boss1.lastX = app.boss1.x
        app.boss1.lastY = app.boss1.y


#decreases ability cooldowns
def abilityCooldowns(app):

    if app.lasers1.currentCD > 0:
        app.lasers1.currentCD -= 1
    
    #charaterUpgrades
    if app.freezingLazers1.bossFreezeCD > 0:
        app.freezingLazers1.bossFreezeCD -= 1

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

            #chracterUpgrades - freezing lasers
            if app.freezingLazers1.bossFreezeCD > 0:
                bossXVelocity *= app.freezingLazers1.bossSpeedMultiplier
                bossYVelocity *= app.freezingLazers1.bossSpeedMultiplier

            #move Boss
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
        app.charNode.color = app.charNode.baseColor
        app.charHealth = 0
        app.situation = 1

def checkBossDead(app):
    if app.boss1.health <= 0:
        app.bossNode.color = app.bossNode.baseColor
        app.boss1.health = 0
        app.boss1.respawnTimer = 200   
        app.kills += 1  

        #makes sure there are enough upgrades left
        #characterUpgrades
        if getNumUpgradesLeft(app):
            app.situation = 2
            get4Upgrades(app)
#loops through all the lazers and moves them
#checks if any lazers collide with the boss and deals damage to the boss if so
def moveLasers(app):

    i = 0
    while i < len(app.lasers1.lasers):

        app.lasers1.lasers[i][0] += math.cos(app.lasers1.lasers[i][2]) * app.lasers1.speed
        app.lasers1.lasers[i][1] -= math.sin(app.lasers1.lasers[i][2]) * app.lasers1.speed
        
        #if laser hits boss
        if app.boss1.health and distance(app, app.boss1.x, app.boss1.y, app.lasers1.lasers[i][0], app.lasers1.lasers[i][1]) < app.boss1.size: 

            #does damage
            app.boss1.health -= app.lasers1.dmg
            app.lasers1.lasers.pop(i)
            checkBossDead(app)
        

        #lasers expires after some time
        elif app.lasers1.lasers[i][3] >= 200:
            app.lasers1.lasers.pop(i)
        else:
            app.lasers1.lasers[i][3] += 1
            i+=1



#=======================================
#GENERAL HELPER FUNTIONS
#=======================================

def pythagoreanTheorem(x, y):
    return (x**2 + y**2)**0.5

def distance(app, x1, y1, x2, y2):
    return pythagoreanTheorem(x2-x1, y2-y1)

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
#walls
#=======================================

def generateWalls(app):

    app.walls = set()

    rows = len(app.matrix)
    cols = len(app.matrix[0])

    c = 0
    for r in range(rows):
        app.matrix[r][c].traversable = False
        app.matrix[r][c].color = "black"
        app.matrix[r][c].baseColor = "black"
        app.walls.add(app.matrix[r][c])

    c = cols-1
    for r in range(rows):
        app.matrix[r][c].traversable = False
        app.matrix[r][c].color = "black"
        app.matrix[r][c].baseColor = "black"
        app.walls.add(app.matrix[r][c])

    r = 0
    for c in range(cols):
        app.matrix[r][c].traversable = False
        app.matrix[r][c].color = "black"
        app.matrix[r][c].baseColor = "black"
        app.walls.add(app.matrix[r][c])

    r = rows - 1
    for c in range(cols):
        app.matrix[r][c].traversable = False
        app.matrix[r][c].color = "black"
        app.matrix[r][c].baseColor = "black"
        app.walls.add(app.matrix[r][c])

    r = 6
    for c in range(2, 7):
        app.matrix[r][c].traversable = False
        app.matrix[r][c].color = "black"
        app.matrix[r][c].baseColor = "black"
        app.walls.add(app.matrix[r][c])

#=======================================
#pathfinding
#=======================================

#creates a gird of node objects
def generateGrid(app):

    #variables
    if True:
        app.nodeWidth = 100
        app.nodeHeight = 100
        app.numBlocksWide = app.backroundWidth//app.nodeWidth
        app.numBlocksHigh = app.backroundHeight//app.nodeHeight
        app.matrix = []
        app.charNode = None
        app.targetNode = None

        app.charPath = []

    for j in range(app.numBlocksHigh):
        app.matrix.append([])
        for k in range(app.numBlocksWide):
            app.matrix[j].append(Node(k, j))

#draws the grid of node objects
def drawGrid(app):

    setX = app.width/2 - app.backroundWidth/2
    y = app.gameHeight/2 - app.backroundHeight/2

    for j in range(app.numBlocksHigh):
        x = setX
        for k in range(app.numBlocksWide):
    
            #sets the color of the node
            color = app.matrix[j][k].color

            if app.charPath:
                for node in app.charPath:
                    if (k, j) == (node.x, node.y):
                        color = "white"

            drawRect(x - app.frameshiftX, y - app.frameshiftY, app.nodeWidth, app.nodeHeight, border = "black", fill = color, opacity = 30)
            x += app.nodeWidth

        y += app.nodeHeight

#returns a tuple of the coordinates that the chracter is in
def findCharNode(app):

    x = app.frameshiftX + app.backroundWidth/2
    y = app.frameshiftY + app.backroundHeight/2

    col = int(x // app.nodeWidth)
    row = int(y // app.nodeHeight)

    #checks to see if the node is in bounds of the grid
    if 0 <= col < app.numBlocksWide and 0 <= row < app.numBlocksHigh:

        if app.matrix[row][col].traversable == False:
            app.frameshiftX = app.lastFrameshiftX
            app.frameshiftY = app.lastFrameshiftY
        else:
            if app.charNode:
                app.charNode.color = app.charNode.baseColor
            app.charNode = app.matrix[row][col]
            app.charNode.color = "blue"

#sets the coordinates that the boss is in
def findBossNode(app):

    x = app.boss1.x + app.backroundWidth/2 - app.width/2
    y = app.boss1.y + app.backroundHeight/2 - app.gameHeight/2

    col = int(x // app.nodeWidth)
    row = int(y // app.nodeHeight)

    #checks to see if the node is in bounds of the grid
    if 0 <= col < app.numBlocksWide and 0 <= row < app.numBlocksHigh:

        if app.matrix[row][col].traversable == False:
            app.boss1.x = app.boss1.lastX
            app.boss1.y = app.boss1.lastY
        else:
            if app.bossNode:
                app.bossNode.color = app.bossNode.baseColor
            app.bossNode = app.matrix[row][col]
            app.bossNode.color = "purple"

def setTargetNode(app, col, row):

    #checks to see if the node is in bounds of the grid
    if 0 <= col < app.numBlocksWide and 0 <= row < app.numBlocksHigh:
        if app.targetNode:
            app.targetNode.color = app.targetNode.baseColor
        app.targetNode = app.matrix[row][col]
        app.targetNode.color = "red"

def findTargetNode(app, targetX, targetY):

    deltaX = targetX - app.charX
    deltaY = targetY - app.charY

    xDistanceFromCenterToTopLeft = app.frameshiftX + app.backroundWidth/2
    yDistanceFromCenterToTopLeft = app.frameshiftY + app.backroundHeight/2

    x = deltaX + xDistanceFromCenterToTopLeft
    y = deltaY + yDistanceFromCenterToTopLeft

    col = int(x // app.nodeWidth )
    row = int(y // app.nodeHeight )

    return (col, row)

def checkCanRightClick(app, row, col):

    if (0 < col or col >= app.numBlocksWide or 0 > row or row >= app.numBlocksHigh):
        return False

    if app.matrix[row][col].traversable == False:
        return False
    
    return True

#A* pathfinding algorithm
def pathfinding(app, startNode, endNode):

    open = []
    closed = []
    open.append(startNode)
    startNode.gCost = 0

    while len(open) > 0:

        #sets cur to the node in open that has the lowest f-cost
        cur = open[0]
        for i in range(1, len(open)):
            if open[i].fCost < cur.fCost:
                cur = open[i]
            elif open[i].fCost == cur.fCost:
                if open[i].hCost < cur.hCost:
                    cur = open[i]

        open.remove(cur)
        closed.append(cur)

        if cur == endNode:
            return path(app, startNode, endNode)

        #loops through the neighbors of the cur node
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if (dx, dy) != (0, 0):
                    neighborY = cur.y + dy
                    neighborX = cur.x + dx
                    if 0 <= neighborY < len(app.matrix) and 0 <= neighborX < len(app.matrix[0]):
                        neighbor = app.matrix[neighborY][neighborX]

                        #pass if the neighbor is not a legal move
                        if canWalkTo(app, cur, neighbor) == False or neighbor in closed:
                            continue
                        else:
                            potentialNewGCost = cur.gCost + getStraightDistance(cur, neighbor)

                            if (neighbor in open and potentialNewGCost < neighbor.gCost) or neighbor not in open:

                                neighbor.gCost = potentialNewGCost
                                neighbor.hCost = getStraightDistance(cur, endNode)
                                neighbor.clacFCost()
                                neighbor.parent = cur

                                if neighbor not in open:
                                    open.append(neighbor)
        
#checks if you can get to a neighboring node from a starting Node
def canWalkTo(app, startingNode, targetNode):

    #if the target Node is not traversable
    if targetNode.traversable == False:
        return False
    
    #if the target node is diagonal but there is a corner Node in the way
    #can't move diagonally across corners
    dx = targetNode.x - startingNode.x
    dy = targetNode.y - startingNode.y

    if dx != 0 and dy != 0:

        sideNode1 = app.matrix[startingNode.y][targetNode.x]
        sideNode2 = app.matrix[targetNode.y][startingNode.x]

        if sideNode1.traversable == False or sideNode2.traversable == False:
            return False

    return True

#finds the distanace between 2 nodes if there are no obsticals
def getStraightDistance(nodeA, nodeB):

    sum = 0

    deltaX = abs(nodeA.x - nodeB.x)
    deltaY = abs(nodeA.y - nodeB.y)

    #summing up diagonal lengths
    while deltaX > 0 and deltaY > 0:
        deltaX -= 1
        deltaY -= 1

        sum += 14

    #summing up axial lengths
    sum += (deltaX * 10)
    sum += (deltaY * 10)

    return sum

#creates a list of nodes that the char has to travel to
def path(app, begin, cur):

    pathList = []

    while (cur != begin):
        pathList.append(cur)
        cur = cur.parent

    return pathList

#removes the next node to move to from the list and moves there
def pathfindingMovement(app):

    cur = app.charPath.pop()

    xDistanceFromGridTopLeft = cur.x * app.nodeWidth + app.nodeWidth/2
    yDistanceFromGridTopLeft = cur.y * app.nodeHeight + app.nodeHeight/2

    x = app.width/2 - app.backroundWidth/2 - app.frameshiftX + xDistanceFromGridTopLeft
    y = app.gameHeight/2 - app.backroundHeight/2 - app.frameshiftY + yDistanceFromGridTopLeft

    setTarget(app, x, y)
    setMoveTo(app)

# #removes the next node to move to from the list and moves there
def setBossPathfindingMovement(app):

    cur = app.bossPath.pop()
    app.boss1.targetGridX = cur.x
    app.boss1.targetGridY = cur.y

def bossPathfindingMovement(app):

    xDistanceFromGridTopLeft = app.boss1.targetGridX * app.nodeWidth + app.nodeWidth/2
    yDistanceFromGridTopLeft = app.boss1.targetGridY * app.nodeHeight + app.nodeHeight/2

    app.boss1.targetX = app.width/2 - app.backroundWidth/2 - app.frameshiftX + xDistanceFromGridTopLeft
    app.boss1.targetY = app.gameHeight/2 - app.backroundHeight/2 - app.frameshiftY + yDistanceFromGridTopLeft

    x = app.boss1.x - app.frameshiftX
    y = app.boss1.y - app.frameshiftY

    deltaX = (app.boss1.targetX-x)
    deltaY = (app.boss1.targetY-y)

    deltaY = -deltaY 

    hypotenuse = pythagoreanTheorem(deltaX, deltaY)
    
    if hypotenuse == 0:
        app.boss1.x, app.boss1.y = app.boss1.targetX + app.frameshiftX, app.boss1.targetY + app.frameshiftY
        app.boss1.isMoving = False
    else:
        if deltaX >= 0:
            app.boss1.targetAngle = math.asin(deltaY/hypotenuse)
        else:
            app.boss1.targetAngle = math.pi - math.asin(deltaY/hypotenuse)
        
        graphicsHorizontalMovement = deltaX/hypotenuse * app.boss1.speed
        graphicsVerticalMovement = -(deltaY/hypotenuse * app.boss1.speed)

        #move Boss
        if distance(app, app.boss1.x - app.frameshiftX, app.boss1.y - app.frameshiftY, app.boss1.targetX, app.boss1.targetY) > app.boss1.speed:

            app.boss1.x += graphicsHorizontalMovement
            app.boss1.y += graphicsVerticalMovement
        else:

            app.boss1.x, app.boss1.y = app.boss1.targetX + app.frameshiftX, app.boss1.targetY + app.frameshiftY
            app.boss1.isMoving = False
        
        bossAttack(app)

#=======================================#=======================================
##charaterUpgrades
#=======================================#=======================================

#Uprgrade selector
#redrawAll
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

#redrawAll
def drawCharUpgrades(app, x, i):

    drawLabel(app.charUpgrades1.fourUpgrades[i].line1, x, app.height/2 - app.height*1/6, size = 25, bold = True)
    drawLabel(app.charUpgrades1.fourUpgrades[i].line2, x, app.height/2 - app.height*1/6 + 40, size = 25, bold = True)

#called by on mouse press
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

def checkIfHoverOverUpgrade(app, mouseX, mouseY):
    #returns the index of the box you are hovering over

    i = findBoxOfMouse(app, mouseX, mouseY)

    app.upgradeBoxes1.highlighted = i

#returns the index of the box you are hovering over
def findBoxOfMouse(app, mouseX, mouseY):

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

#checks how many upgrades that the character doesn't have
def getNumUpgradesLeft(app):

    counter = 0
    
    for i in range(len(app.charUpgrades1.list)):
        if app.charUpgrades1.list[i] == False:
            counter += 1

    if counter >= 4:
        return True
    return False

#=======================================
#MAIN
#=======================================
def main():
    runApp()

main()












