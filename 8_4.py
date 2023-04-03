#encoding: utf-8
"""Увага! Англійська клавіатура"""
from __future__ import division

from nodebox.graphics import *
import pymunk
import pymunk.pyglet_util
import random, time, math
space = pymunk.Space()

def createBody(x,y,shape,*shapeArgs):
    body = pymunk.Body()
    body.position = x, y
    s = shape(body, *shapeArgs)
    #s = pymunk.Poly.create_box(body, size=(40, 20))
    s.mass = 1
    s.friction = 1
    space.add(body, s)
    return s #shape!!!

s0=createBody(300, 300, pymunk.Poly, ((-20,-5),(-20,5),(20,15),(20,-15)))
s3=createBody(200, 300, pymunk.Poly, ((-20,-5),(-20,5),(20,15),(20,-15)))
s3.color = (0, 255, 0, 255)
s1=createBody(300, 200, pymunk.Circle, 10, (0,0))
s2=createBody(200, 200, pymunk.Circle, 10, (0,0))
s2.color = (255, 0, 0, 255)
def getAngle(x,y,x1,y1):
    return math.atan2(y1-y, x1-x)

def getDist(x,y,x1,y1):
    return ((x-x1)**2+(y-y1)**2)**0.5

def inCircle(x,y,cx,cy,R):
    if (x-cx)**2+(y-cy)**2 < R**2:
        return True
    return False

def strategy(b=s3.body):
    v=100
    a=b.angle
    b.velocity=v*cos(a), v*sin(a)
    x,y=b.position
    R=getDist(x,y,350,250)
    #print R, b.angle
    line(x,y,*s1.body.position,stroke=Color(0))
    if canvas.frame%100==0:
        if R>180:
            b.angle=getAngle(x,y,350,250)
        else:
            b.angle=getAngle(x,y,*s1.body.position) #2*math.pi*random.random()

def strategy2(b=s3.body): # blind
    v=100
    a=b.angle
    b.velocity=v*cos(a), v*sin(a)
    x,y=b.position
    R=getDist(x,y,350,250)
    ellipse(x, y, 200, 200, stroke=Color(0.5))
    line(x,y,x+100*cos(a),y+100*sin(a),stroke=Color(0.5))
    line(x,y,x+100*cos(a+0.5),y+100*sin(a+0.5),stroke=Color(0.5))
    line(x,y,x+100*cos(a-0.5),y+100*sin(a-0.5),stroke=Color(0.5))
    if canvas.frame%100==0:
        if R>180:
            b.angle=getAngle(x,y,350,250)
        else:
            if inCircle(s1.body.position[0], s1.body.position[1], x, y, 100):
                b.angle=getAngle(x,y,*s1.body.position)
            else:
                b.angle=2*math.pi*random.random()


draw_options = pymunk.pyglet_util.DrawOptions()
#draw_options.shape_static_color=(0,0,0)
v=0
def draw(canvas):
    global body,vx,vy
    #background(1)
    canvas.clear()
    nofill()
    ellipse(350, 250, 350, 350, stroke=Color(0))
    if canvas.keys.char=="a":
        s0.body.angle-=0.1
    if canvas.keys.char=="d":
        s0.body.angle+=0.1
    if canvas.keys.char=="w":
        s0.body.velocity=s0.body.velocity[0]+10*cos(s0.body.angle), s0.body.velocity[1]+10*sin(s0.body.angle)
    if canvas.mouse.button==LEFT:
        s0.body.angle=getAngle(s0.body.position[0],s0.body.position[1],*canvas.mouse.xy)
        s0.body.velocity=s0.body.velocity[0]+10*cos(s0.body.angle), s0.body.velocity[1]+10*sin(s0.body.angle)

    strategy2()

    for s in s0,s1,s2,s3:
        s.body.velocity=s.body.velocity[0]*0.9, s.body.velocity[1]*0.9
        s.body.angular_velocity=s.body.angular_velocity*0.9
        #s.body.update_velocity(s.body, (0.,0.), 0.9, 0.02)

    space.step(0.02)
    space.debug_draw(draw_options)

canvas.size = 700, 500
canvas.run(draw)