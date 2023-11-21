from cmu_graphics import *
import math

#==============================================================================
#==============================================================================
#Classes
#==============================================================================
#==============================================================================

class car:
    pass

class boss:
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
    
    #CAR VARIABLES
    if True:
        app.carColor = 'blue'
        app.x = app.width/2
        app.y = app.height/2
        
        app.carDirectionAngleRadians = math.pi/2
        app.carDirectionAngleDegrees = 0
        
        app.blinker = False
        app.rightBlinker = False
        app.leftBlinker = False
        app.headlights = False

        app.carSpeed = 0
        app.maxSpeed = 3
        app.carAcceleration = 0
        app.carDownVelocity = 0
        app.carRightVelocity = 0
        
        #LAZERS
        app.lazers = []
    
    app.isBoss = False
    
#=======================================
#MODEL HELPER FUNTIONS
#=======================================

def resetBoss(app):
    app.bossDMG = 33
    app.bossTotalHealth = 100
    app.bossHealth = 100
    app.bossSpeed = 1
    app.bossX = app.width/2
    app.bossY = app.height/2

#==============================================================================
#==============================================================================
#DRAWING
#==============================================================================
#==============================================================================
def redrawAll(app):

    drawMap(app)
    
    if app.isBoss:
        drawBoss(app)
        drawBossHealthbar(app)
    
    if app.headlights:
        headlights(app)
    drawCar(app)
    drawCarDirection(app)
    drawSpeedometer(app)
    timeUI(app)

    drawLazers(app)

    if app.paused:
        pauseScreen(app)
    
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

#DRAWING CAR
def drawCar(app):
    drawRect(app.x, app.y, 10, 16, align = 'center', rotateAngle = -app.carDirectionAngleDegrees + 90, fill = 'blue')
    drawCarDetails(app)
    
#TOP RIGHT UI================
#DRAW SPEEDOMETER
def drawSpeedometer(app):
    
    drawLabel(f'CAR SPEED: {app.displaySpeed}', app.width - 10, 20, size = 16, align = 'top-right')
#UI Car direction
def drawCarDirection(app):
    
    drawLabel(f'CAR ANGLE(DEGREES): {app.displayDegees}', app.width - 10, 40, size = 16, align = 'top-right')
#TIME
def timeUI(app):
    drawLabel(f'TIME: {app.displayTime}', app.width - 10, 60, size = 16, align = 'top-right')

#PAUSE SCREEN
def pauseScreen(app):
    drawRect(0, 0, app.width, app.height, fill = 'black', opacity = 40)
    drawLabel('GAME IS PAUSED', app.width/2, app.height/2-100, size = 40, bold = True)
    
#CAR DETAILS
def drawCarDetails(app):
    drawRect(app.x, app.y, 10, 10, align = 'center', rotateAngle = -app.carDirectionAngleDegrees + 90, fill = 'black')
    drawCarLights(app)
    
#draw car lights
def drawCarLights(app):
    leftLightX = math.cos(app.carDirectionAngleRadians+0.4) * 9 + app.x
    leftLightY = -math.sin(app.carDirectionAngleRadians+0.4) * 9 + app.y
    
    rightLightX = math.cos(app.carDirectionAngleRadians-0.4) * 9 + app.x
    rightLightY = -math.sin(app.carDirectionAngleRadians-0.4) * 9 + app.y
    
    
    drawCircle(leftLightX, leftLightY, 1, fill = 'yellow')
    drawCircle(rightLightX, rightLightY, 1, fill = 'yellow')
    
    #blinker
    if True:
        if app.blinker and app.time%5 == 0:
            if app.leftBlinker == True:
                drawCircle(leftLightX, leftLightY, 2, fill = 'orange')
            if app.rightBlinker == True:
                drawCircle(rightLightX, rightLightY, 2, fill = 'orange')
             
#LAZERS   
def drawLazers(app):
    for lazer in app.lazers:
        lazerXStart = lazer[0] - math.cos(lazer[2]) * 3
        lazerYStart = lazer[1] + math.sin(lazer[2]) * 3
        
        lazerXEnd = lazer[0] + math.cos(lazer[2]) * 3
        lazerYEnd = lazer[1] - math.sin(lazer[2]) * 3
        
        drawLine(lazerXStart, lazerYStart, lazerXEnd, lazerYEnd, fill = 'red')
                
#draw headlights
def headlights(app):
    for i in range(100):
        drawArc(app.x, app.y, 200 - i *2, 200 - i *2, app.carDirectionAngleDegrees-30, 60, fill='yellow', opacity = i/30)
        
#drawBoss
def drawBoss(app):
    drawCircle(app.bossX, app.bossY, 40, align = 'center', fill = 'purple')
    
#boss healthbar
def drawBossHealthbar(app):
    
    drawRect(app.width/2, 40, 800, 30, align = 'center', border = 'black', borderWidth = 50)
    
    rectWidth = 800/app.bossTotalHealth
    startX = app.width/2-400+rectWidth/2
    
    for i in range(app.bossTotalHealth):
        
        if i < app.bossHealth:
            color = 'red'
        elif i > app.bossHealth:
            color = rgb(200, 200, 200)
        
        drawRect(startX + i*rectWidth, 40, rectWidth, 30, align = 'center', fill = color)
        
    drawLabel(f'{app.bossHealth} / {app.bossTotalHealth}', app.width/2, 40, size = 20)

#==============================================================================
#==============================================================================
#CONTROLLERS
#==============================================================================
#==============================================================================
def onKeyPress(app, key):
    if key == 'p':
        app.paused = not(app.paused)
        
    #headlights
    if key == 'l':
        app.headlights = not(app.headlights)
    
    #lazers
    if key == "space":
        app.lazers.append([app.x, app.y, app.carDirectionAngleRadians])
    
    #Blinker
    if True:
        if key == 'b':
            app.blinker = not(app.blinker)
        
def onKeyHold(app, keys):

    if 'up' in keys:
        if app.carAcceleration < 0.1:
            app.carAcceleration += 0.01
    if 'down' in keys:
        if app.carAcceleration > -0.1:
            app.carAcceleration -= 0.01
        
    # TURNING
    if 'left' in keys and gasIsOn(app, keys):
        app.carDirectionAngleRadians += 0.1
    if 'right' in keys and gasIsOn(app, keys):
        app.carDirectionAngleRadians -=0.1
        
    #lazers
    if "space" in keys:
        app.lazers.append([app.x, app.y, app.carDirectionAngleRadians])
        
    #blinker
    if True:
        if 'left' in keys:
            app.leftBlinker = True
        if 'right' in keys:
            app.rightBlinker = True
        
def onKeyRelease(app, key):
    
    if key == 'up' or key == 'down':
        app.carAcceleration = 0
    
    
    if key == 'left':
        app.leftTurn = None
    if key == 'right':
        app.rightTurn = None      
        
    #Blinker
    if True:
        if key == 'left':
            app.leftBlinker = False
        if key == 'right':
            app.rightBlinker = False
        
def onStep(app):
    
    #makes sure the Degrees is equal to the angle
    app.carDirectionAngleDegrees = math.degrees(app.carDirectionAngleRadians)
    
    if app.paused == False:
        
        app.time+=1
        
        #CHANGE DISPLAY
        if app.time %5 == 0:
            app.displaySpeed = roundToThousands(app, app.carSpeed)
            app.displayDegees = roundToThousands(app, app.carDirectionAngleDegrees%360)
            app.displayTime = roundToThousands(app, app.time)
    
        #CAR MOVEMENTS
        app.x += app.carRightVelocity
        app.y += app.carDownVelocity
        
        #Acceleration -> velocity
        carVelocityIncreaseCalculator(app)
        
        #FRICTION
        onstepFrictionCalculator(app)
        
        #MOVE LAZERS
        moveLazers(app)
        
        #SPAWNS BOSS AT TIME = 300
        if app.time == 100:
            resetBoss(app)
            app.isBoss = True
        if app.isBoss:
            bossMove(app)
        

#=======================================
#CONTROLLER HELPER FUNTIONS
#=======================================

def carVelocityIncreaseCalculator(app):
    
    #CANT GO OVER MAX SPEED
    app.carSpeed = pythagoreanTheorem(app, app.carRightVelocity, app.carDownVelocity)

    # dVx = cos(angle) * a 
    app.carRightVelocity += math.cos(app.carDirectionAngleRadians) * app.carAcceleration
    # dVy = sin(angle) * a 
    app.carDownVelocity -= math.sin(app.carDirectionAngleRadians) * app.carAcceleration   
    
    if app.carRightVelocity > abs(math.cos(app.carDirectionAngleRadians)) * app.maxSpeed:
        app.carRightVelocity = abs(math.cos(app.carDirectionAngleRadians)) * app.maxSpeed
    if app.carRightVelocity < -abs(math.cos(app.carDirectionAngleRadians)) * app.maxSpeed:
        app.carRightVelocity = -abs(math.cos(app.carDirectionAngleRadians)) * app.maxSpeed
        
    if app.carDownVelocity > abs(math.sin(app.carDirectionAngleRadians)) * app.maxSpeed:
        app.carDownVelocity = abs(math.sin(app.carDirectionAngleRadians)) * app.maxSpeed
    if app.carDownVelocity < -abs(math.sin(app.carDirectionAngleRadians)) * app.maxSpeed:
        app.carDownVelocity = -abs(math.sin(app.carDirectionAngleRadians)) * app.maxSpeed
        
    # CANT GO OUTTA BOUNDS
    carCantGoOuttaBounds(app)

def onstepFrictionCalculator(app):
    frictionConstant = 0.03
    if app.carRightVelocity > 0:
        app.carRightVelocity -= frictionConstant
    if app.carRightVelocity < 0:
        app.carRightVelocity += frictionConstant
    if app.carDownVelocity > 0:
        app.carDownVelocity -= frictionConstant
    if app.carDownVelocity < 0:
        app.carDownVelocity += frictionConstant
        
    # if abs(app.carRightVelocity) < frictionConstant:
    #     app.carRightVelocity = 0
    # if abs(app.carDownVelocity) < frictionConstant:
    #     app.carDownVelocity = 0

def gasIsOn(app, keys):
    if 'down' in keys or 'up' in keys:
        return True
    return False
    
def carCantGoOuttaBounds(app):
    if app.x < 10:
        app.x = 10
    if app.x > app.width-10:
        app.x = app.width-10
    if app.y < 10:
        app.y = 10
    if app.y > app.height-10:
        app.y = app.height-10
        
def moveLazers(app):
    i = 0
    while i < len(app.lazers):
        app.lazers[i][0] = app.lazers[i][0] + math.cos(app.lazers[i][2]) * 10
        app.lazers[i][1] = app.lazers[i][1] - math.sin(app.lazers[i][2]) * 10
        
        #if lazer hits boss
        if app.isBoss and distance(app, app.bossX, app.bossY, app.lazers[i][0], app.lazers[i][1]) < 40:
            app.bossHealth -= 1
            app.lazers.pop(i)
            if app.bossHealth <= 0:
                app.isBoss = False
        
        #delete lazer if out of bounds
        elif app.lazers[i][0]>app.width or app.lazers[i][0] < 0:
            app.lazers.pop(i)
        elif app.lazers[i][1]>app.height or app.lazers[i][1] < 0:
            app.lazers.pop(i)
        else:
            i+=1

    
            
            
            
def bossMove(app):
    
    if app.isBoss:
    
        verticalLength = (app.y-app.bossY)
        horizontalLength = (app.x-app.bossX) 
        hypotenuse = pythagoreanTheorem(app, (app.x-app.bossX), (app.y-app.bossY))
        
        bossXVelocity = horizontalLength/hypotenuse * app.bossSpeed
        bossYVelocity = -verticalLength/hypotenuse * app.bossSpeed
        
        bossRightVelocity = bossXVelocity
        bossDownVelocity = -bossYVelocity
        
        app.bossX += bossRightVelocity
        app.bossY += bossDownVelocity
        
        bossAttack(app)
        
def bossAttack(app):
    if distance(app, app.bossX, app.bossY, app.x, app.y) < 40:
        app.dead = True
        app.paused = True
    

#=======================================
#GENERAL HELPER FUNTIONS
#=======================================
def pythagoreanTheorem(app, x, y):
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