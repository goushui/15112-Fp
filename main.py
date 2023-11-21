from cmu_graphics import *
import math


#==============================================================================
#==============================================================================
#START
#==============================================================================
#==============================================================================

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
        self.size = 10

        #direction
        self.moveToCoords = None
        self.moveToAngle = None

        self.targetCoords = None
        self.targetAngle = None

class lazers:

    def __init__(self):

        self.lazers = []
        self.dmg = 5
        self.color = "red"
        self.width = 1
        self.speed = 2
        self.cooldown = 0

#==============================================================================
#==============================================================================
#START
#==============================================================================
#==============================================================================
def onAppStart(app):
    
    #reize window
    app.width = 1400
    app.height = 900
    
    reset(app)
    
def reset(app):

    app.boss1 = boss()
    app.character1 = character()
    app.lazers1 = lazers()
    
    app.stepPerSecond = 30
    app.paused = True
    app.time = 0
    
    #DISPLAY
    app.displaySpeed = 0
    app.displayDegees = 0
    app.displayTime = 0

    
    #CHAR VARIABLES
    if True:
        app.character1.x = app.width/2
        app.character1.y = app.height/2
        
        #LAZERS
        app.lazers = []

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

    drawCharacterHealthbar(app)
    if app.character1.health:
        drawCharacter(app)

    if app.boss1.health:
        drawBoss(app)
        drawBossHealthbar(app)

    if app.lazers1.lazers:
        drawLazers(app)



    if app.paused:
        pauseScreen(app)
    
#=======================================
#DRAWING HELPER FUNTIONS
#=======================================

#DRAWING MAP
def drawMap(app):
    drawRect(0, 0, app.width, app.height, fill = 'black', opacity = 70)
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

#LAZERS   
def drawLazers(app):
    for lazer in app.lazers1.lazers:
        lazerXStart = lazer[0] - math.cos(lazer[2]) * 3
        lazerYStart = lazer[1] + math.sin(lazer[2]) * 3
        
        lazerXEnd = lazer[0] + math.cos(lazer[2]) * 3
        lazerYEnd = lazer[1] - math.sin(lazer[2]) * 3
        
        drawLine(lazerXStart, lazerYStart, lazerXEnd, lazerYEnd, fill = app.lazers1.color)

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
    

#==============================================================================
#==============================================================================
#CONTROLLERS
#==============================================================================
#==============================================================================
def onKeyPress(app, key):
    if key == 'p':
        app.paused = not(app.paused)

    #lazers
    if key == 'q' and app.lazers1.cooldown == 0:
        app.lazers1.cooldown = 10
        app.lazers1.lazers.append([app.character1.x, app.character1.y, app.character1.targetAngle])


def onMousePress(app, mouseX, mouseY, button):
    
    if button == 2:
        setMoveTo(app, mouseX, mouseY)

def setMoveTo(app, mouseX, mouseY):

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

#def onKeyHold(app, keys):

        
# def onKeyRelease(app, key):
    

#=======================================
#onStep
#=======================================     
def onStep(app):

    if app.paused:
        pass

    else:
        
        app.time += 1
        abilityCooldowns(app)

        if app.character1.moveToCoords:
            moveCharacter(app)

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

    if app.lazers1.cooldown > 0:
        app.lazers1.cooldown -= 1


def moveCharacter(app):

    x, y = app.character1.moveToCoords

    if distance(app, app.character1.x, app.character1.y, x, y) > app.character1.speed:

        app.character1.x += (app.character1.speed * math.cos(app.character1.moveToAngle))
        app.character1.y += -(app.character1.speed * math.sin(app.character1.moveToAngle))
    else:
        app.character1.x = x
        app.character1.y = y

#loops through all the lazers and moves them
#checks if any lazers collide with the boss and deals damage to the boss if so
def moveLazers(app):
    i = 0
    while i < len(app.lazers1.lazers):
        app.lazers1.lazers[i][0] = app.lazers1.lazers[i][0] + math.cos(app.lazers1.lazers[i][2]) * 10
        app.lazers1.lazers[i][1] = app.lazers1.lazers[i][1] - math.sin(app.lazers1.lazers[i][2]) * 10
        
        #if lazer hits boss
        if app.boss1.health and distance(app, app.boss1.x, app.boss1.y, app.lazers1.lazers[i][0], app.lazers1.lazers[i][1]) < app.boss1.size:
            app.boss1.health -= app.lazers1.dmg
            app.lazers1.lazers.pop(i)
            checkBossDead(app)
        
        #delete lazer if out of bounds
        elif app.lazers1.lazers[i][0]>app.width or app.lazers1.lazers[i][0] < 0:
            app.lazers1.lazers.pop(i)
        elif app.lazers1.lazers[i][1]>app.height or app.lazers1.lazers[i][1] < 0:
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
        
        bossRightVelocity = bossXVelocity
        bossDownVelocity = -bossYVelocity
        
        app.boss1.x += bossRightVelocity
        app.boss1.y += bossDownVelocity
        
        bossAttack(app)

#checks if boss is in range to do a melee attack 
def bossAttack(app):
    if distance(app, app.boss1.x, app.boss1.y, app.character1.x, app.character1.y) < app.boss1.size:
        app.character1.health -= app.boss1.meleeDmg
        checkCharacterDead(app)

def checkCharacterDead(app):
    if app.character1.health <= 0:
        app.character1.health = 0
        app.paused = True

def checkBossDead(app):
    if app.boss1.health <= 0:
        app.boss1.health = 0
        app.boss1.respawnTimer = 200        


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