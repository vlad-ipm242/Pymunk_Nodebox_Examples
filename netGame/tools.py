#encoding: utf-8
import socket
from nodebox.graphics import *
import pymunk, random, math
import pymunk.pyglet_util
space = pymunk.Space()

def send(x):
    if x=="": return
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 50007))
    s.sendall(str(x))
    x=s.recv(255)
    s.close()
    return x

def createBody(x,y,shape,*shapeArgs):
    body = pymunk.Body()
    body.position = x, y
    s = shape(body, *shapeArgs)
    s.mass = 1
    s.friction = 1
    space.add(body, s)
    return s #shape!!!

s0=createBody(300, 200, pymunk.Circle, 10, (0,0))
s0.color = (255, 0, 0, 255)
s1=createBody(300, 300, pymunk.Poly, ((-20,-5),(-20,5),(20,15),(20,-15)))
s1.score=0
s1.color = (0, 0, 255, 255)
s2=createBody(200, 300, pymunk.Poly, ((-20,-5),(-20,5),(20,15),(20,-15)))
s2.color = (0, 255, 0, 255)
s2.score=0
s3=createBody(200, 200, pymunk.Poly, ((-20,-5),(-20,5),(20,15),(20,-15)))
s3.color = (100, 100, 0, 255)
s3.score=0

S={s0,s1,s2,s3}

def simFriction():
    for s in S:
        s.body.velocity=s.body.velocity[0]*0.9, s.body.velocity[1]*0.9
        s.body.angular_velocity=s.body.angular_velocity*0.9
        if s.body.position[0]<0:
           s.body.position = 700, s.body.position[1]
        if s.body.position[0]>700:
            s.body.position = 0, s.body.position[1]
        if s.body.position[1]<0:
            s.body.position= s.body.position[0], 500
        if s.body.position[1]>500:
            s.body.position= s.body.position[0], 0

def getAngle(x,y,x1,y1):
    return math.atan2(y1-y, x1-x)

def getDist(x,y,x1,y1):
    return ((x-x1)**2+(y-y1)**2)**0.5

def inCircle(x,y,cx,cy,R):
    if (x-cx)**2+(y-cy)**2 < R**2:
        return True
    return False

def inSector(x,y,cx,cy,R,a):
    angle=getAngle(cx,cy,x,y)
    a=a%(2*math.pi)
    angle=angle%(2*math.pi)
    if inCircle(x,y,cx,cy,R) and a-0.5<angle<a+0.5:
        return True
    return False
