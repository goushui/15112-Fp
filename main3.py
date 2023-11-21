from cmu_graphics import *
import math
import random


"""
Why is my game laggy?


to
- make freeze lazers blue
make more dmg lazers wideer


citations:
- framseshift got the idea of moving all the things on the screen from 2022 page
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

        self.speed = 3
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
        self.targetAngle = None

        self.kills = 0

class lazers:

    def __init__(self):

        self.lazers = []
        self.dmg = 50
        self.color = "red"
        self.width = 2
        self.speed = 10
        self.cD = 20

class icons:

    def __init__(self):

        self.x = None
        self.y = None
        self.timer = None
        

class charUpgrades:

    def __init__(self):

        self.list = [True, False, False, False, False, False]
        self.Objects = [app.freezingLazers1, app.lazerDmg1, app.lazerAttackSpeed1, app.fasterMS1, app.increaseHP1, app.dash1]

        self.fourUpgrades

class freezingLazers(charUpgrades):
        
    def __init__(self):
        self.bossSpeedMultiplier = 1
        self.bossFreezeCD = 0

        self.setnBossSpeedMultiplier = 1
        self.setBossFreezeCD = 20

        self.line1 = "lazers freeze"
        self.line2 = "the enemy"

class lazerDmg(charUpgrades):
        
    def __init__(self):
        self.dmgMultiplier = 1.2

        self.line1 = "lazers do"
        self.line2 = "more damage"

class lazerAttackSpeed(charUpgrades):
        
    def __init__(self):
        self.lazerAttackintervalMuliplier = 0.9

        self.line1 = "lazer cooldown"
        self.line2 = "is shorter"

class fasterMS(charUpgrades):
        
    def __init__(self):
        self.speedMuliplier = 1.2

        self.line1 = "character moves"
        self.line2 = "faster"

class increaseHP(charUpgrades):

    def __init__(self):
        self.hpMuliplier = 2

        self.line1 = "character gains"
        self.line2 = "more HP"

class dash(charUpgrades):

    def __init__(self):
        self.distance = 30

        self.line1 = "character gains a "
        self.line2 = "short dash ability"
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

        app.freezingLazers1 = freezingLazers()
        app.lazerDmg1 = lazerDmg()
        app.lazerAttackSpeed1 = lazerAttackSpeed()
        app.fasterMS1 = fasterMS()
        app.increaseHP1 = increaseHP()
        app.dash1 = dash()
    
    app.stepPerSecond = 30
    app.time = 0
    
    app.situation = 0
    
    #CHAR VARIABLES
    if True:
        app.character1.x = app.width/2
        app.character1.y = app.gameHeight/2


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
    drawBotBar(app)

    drawCharacterHealthbar(app)
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
    
#=======================================
#DRAWING HELPER FUNTIONS
#=======================================

#DRAWING MAP
def drawMap(app):
    drawRect(app.map1.dx + 0, app.map1.dy + 0, 2000, 2000, fill = 'black', opacity = 70)
    drawRect(app.map1.dx + 0, app.map1.dy + 300, app.width, 40, fill = 'black')
    drawRect(app.map1.dx + 0, app.map1.dy + 300, app.width, 40, fill = 'white', opacity = 50)
    drawRect(app.map1.dx + 400, app.map1.dy + 0, 40, app.gameHeight, fill = 'black')
    drawRect(app.map1.dx + 400, app.map1.dy + 0, 40, app.gameHeight, fill = 'white', opacity = 50)

#DRAWING Bottom Bar
def drawBotBar(app):
    drawRect(0, app.gameHeight, app.width, app.height - app.gameHeight, fill = 'black', opacity = 100)

#ENDING 1 SCREEN
def drawEnding1(app):
    drawRect(0, 0, app.width, app.height, fill = 'black', opacity = 40)
    drawLabel('GAME OVER', app.width/2, app.height/2-130, size = 40, bold = True, fill = "cyan")
    drawLabel(f'SCORE: {app.character1.kills}', app.width/2, app.height/2-70, size = 40, bold = True, fill = "cyan")

#PAUSE SCREEN
def pauseScreen(app):
    drawRect(0, 0, app.width, app.height, fill = 'black', opacity = 40)
    drawLabel('GAME IS PAUSED', app.width/2, app.height/2-100, size = 40, bold = True)

#DRAWS CHRACTER
def drawCharacter(app):
    drawCircle(app.character1.x, app.character1.y, app.character1.size)

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
    drawCircle(app.boss1.x, app.boss1.y, app.boss1.size, align = 'center', fill = app.boss1.color)
    
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

#character heal;thbar
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
    rectHeight = app.height/1.5

    gapWidth = rectWidth/4

    startX = app.width/2 - gapWidth * 1.5 - rectWidth * 1.5

    for i in range(4):

        addToStartX = i * (gapWidth + rectWidth)
        drawRect(startX + addToStartX, app.height/2, rectWidth, rectHeight, align = "center", fill = "grey")

        drawCharUpgrades(app, addToStartX)

def drawCharUpgrades(app):

    
    drawLabel()

#==============================================================================
#==============================================================================
#CONTROLLERS
#==============================================================================
#==============================================================================
def onKeyPress(app, key):
    if key == 'p':
        if app.situation == 0:
            app.situation = 3
        elif app.situation == 3:
            app.situation = 0

    #lazers
    if key == 'q' and app.lazers1.cD == 0:
        app.lazers1.cooldown = app.lazers1.cD
        app.lazers1.lazers.append([app.character1.x, app.character1.y, app.character1.targetAngle])

def onMousePress(app, mouseX, mouseY, button):
    
    if button == 2:
        setMoveTo(app, mouseX, mouseY)

def setMoveTo(app, mouseX, mouseY):

    app.character1.isMoving = True
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

def onMouseMove(app, mouseX, mouseY):
    setTarget(app, mouseX, mouseY)

def setTarget(app, mouseX, mouseY):

    app.targetCoords = mouseX, mouseY

    deltaX = mouseX - app.character1.x
    deltaY = -(mouseY - app.character1.y)

    hypotenuse = pythagoreanTheorem(deltaX, deltaY)
    
    if deltaX >= 0:
        app.character1.targetAngle = math.asin(deltaY/hypotenuse)
    else:
        app.character1.targetAngle = math.pi - math.asin(deltaY/hypotenuse)

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

        #SPAWNS BOSS AT TIME = 300
        if app.boss1.health == 0:
            app.boss1.respawnTimer -= 1
            if app.boss1.respawnTimer == 0:
                resetBoss(app)

        if app.boss1.health:
            bossMove(app)


#decreases ability cooldowns
def abilityCooldowns(app):

    if app.lazers1.cD > 0:
        app.lazers1.cD -= 1

    if app.freezingLazers1.bossFreezeCD > 0:
        app.freezingLazers1.bossFreezeCD -= 1

#finds the distance between where the chracter is moving to and the character and checks that it is higher then the chracter speed
def characterMove(app):

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
    if app.character1.isMoving:
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
        if app.character1.isMoving:
            app.lazers1.lazers[i][0] -= app.character1.dx
            app.lazers1.lazers[i][1] -= app.character1.dy
        
        #if lazer hits boss
        if app.boss1.health and distance(app, app.boss1.x, app.boss1.y, app.lazers1.lazers[i][0], app.lazers1.lazers[i][1]) < app.boss1.size:
            #checks for freezin lazer
            if app.charUpgrades1.list[0]:
                app.freezingLazers1.bossSpeedMultiplier = app.freezingLazers1.bossSpeedMultiplier
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
    
        verticalLength = (app.character1.y-app.boss1.y)
        horizontalLength = (app.character1.x-app.boss1.x) 
        hypotenuse = pythagoreanTheorem((app.character1.x-app.boss1.x), (app.character1.y-app.boss1.y))
        
        bossXVelocity = horizontalLength/hypotenuse * app.boss1.speed
        bossYVelocity = -verticalLength/hypotenuse * app.boss1.speed

        #freezing lasers
        if app.freezingLazers1.bossFreezeCD > 0:
            bossXVelocity *= app.freezingLazers1.bossSpeedMultiplier
            bossYVelocity *= app.freezingLazers1.bossSpeedMultiplier
        
        bossRightVelocity = bossXVelocity
        bossDownVelocity = -bossYVelocity
        
        app.boss1.x += bossRightVelocity
        app.boss1.y += bossDownVelocity

        #frameShift Boss
        if app.character1.isMoving:
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
        app.situation = 2

def get4Upgrades(app):

    index = random.randint(3, 9)

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