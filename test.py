from cmu_graphics import *



app.character1.dx += (app.character1.speed * math.cos(app.character1.moveToAngle))
app.character1.dy -= (app.character1.speed * math.sin(app.character1.moveToAngle))