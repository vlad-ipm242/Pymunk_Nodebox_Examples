#encoding: utf-8
from __future__ import division

from nodebox.graphics import *
import pymunk
import pymunk.pyglet_util
import random
from math import sin, cos, pi, atan2

space = pymunk.Space()
space.gravity = 0,-981

def create_moto():
    cbody = pymunk.Body()
    cbody.position = 200,400
    circle=pymunk.Circle(cbody,20)
    circle.mass = 100
    circle.friction = 1
    space.add(cbody, circle)
    cbody2 = pymunk.Body()
    cbody2.position = 300,400
    circle2=pymunk.Circle(cbody2,20)
    circle2.mass = 100
    circle2.friction = 1
    c = pymunk.PinJoint(cbody, cbody2, (0, 0), (0, 0))
    space.add(cbody2, circle2, c)
    pbody = pymunk.Body()
    pbody.position = 250,450
    #poly = pymunk.Poly.create_box(pbody, size=(50,20))
    poly=pymunk.Circle(pbody,20)
    poly.mass = 10
    poly.friction = 1
    c2 = pymunk.PinJoint(cbody, pbody, (0, 0), (0, 0))
    c3 = pymunk.DampedSpring(cbody2, pbody, (0, 0), (0, 0), 50, 5000, 300)
    space.add(pbody, poly, c2, c3)
    return pbody, cbody, cbody2

pbody, cbody, cbody2 = create_moto()

def create_poly(x,y,x1,y1):
    body = pymunk.Body()
    body.position = x,y
    body.velocity= x1,y1
    poly = pymunk.Poly.create_box(body, size=(random.randint(10,40),10))
    poly.mass = 10
    poly.friction = 1
    poly.color = (255, 0, 0, 255)
    space.add(body, poly)

def create_static(pos=(0, 0), p1=(-200, 100),p2=(700, 100)):
    body = pymunk.Body(body_type = pymunk.Body.KINEMATIC)
    body.position = pos
    line = pymunk.Segment(body, p1, p2, 3)
    line.friction = 1
    line.color = (0, 255, 0, 255)
    space.add(body, line)

create_static()

draw_options = pymunk.pyglet_util.DrawOptions()

x,y=0,0
blck=False
x2,y2=0,0

def draw(canvas):
    global x, y, blck, x2, y2, pbody, cbody, cbody2
    background(1)

    if canvas.mouse.button==LEFT:
        if not blck==True:
            x,y=canvas.mouse.xy
            blck=True
    if canvas.mouse.dragged and canvas.mouse.button==LEFT:
        x2,y2=canvas.mouse.xy
        stroke(255,0,0,255)
        line(x,y,x2,y2)
    elif blck and x2 and y2:
        create_static(pos=(0, 0), p1=(x, y), p2=(x2, y2))
        blck=False

    if canvas.mouse.button==MIDDLE:
        i,j=canvas.mouse.xy
        create_poly(i, j, 0, 0)

    if canvas.keys.char=="a":
        if canvas.frame%10==0:
            pbody, cbody, cbody2 = create_moto()

    space.step(0.02)

    if canvas.mouse.button==RIGHT:
        x,y=canvas.mouse.x,canvas.mouse.y
        cbody.angular_velocity= -(x-250)/10
        cbody2.angular_velocity= -(x-250)/10

    for b in space.bodies:
        b.position=b.position[0]-1, b.position[1]

    # #space.reindex_static()
    space.debug_draw(draw_options)


canvas.size = 600, 500
canvas.run(draw)
