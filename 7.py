#encoding: utf-8
from __future__ import division

from nodebox.graphics import *
import pymunk
import pymunk.pyglet_util
import random, time
space = pymunk.Space()
space.gravity = 0, -981

def create_moto():
    cbody = pymunk.Body()
    cbody.position = 0+300,100
    circle=pymunk.Circle(cbody, 20)
    circle.mass = 100
    circle.friction = 1
    space.add(cbody, circle)
    cbody2 = pymunk.Body()
    cbody2.position = 100+300,100
    circle2=pymunk.Circle(cbody2, 20)
    circle2.mass = 100
    circle2.friction = 1
    c = pymunk.PinJoint(cbody, cbody2, (0, 0), (0, 0))
    space.add(cbody2, circle2, c)
    pbody = pymunk.Body()
    pbody.position = 50+300,200
    #pbody.center_of_gravity=0,-90
    poly = pymunk.Poly.create_box(pbody, size=(10,200))
    poly.mass = 1
    poly.friction = 1
    c2 = pymunk.PinJoint(cbody, pbody, (0, 0), (0, -50))
    c3 = pymunk.PinJoint(cbody2, pbody, (0, 0), (0, -50))
    space.add(pbody, poly, c2, c3)
    return pbody, cbody, cbody2, c, c2, c3

def create_static(pos=(300, 120), p1=(-200, 0),p2=(300, 0)):
    body = pymunk.Body(body_type = pymunk.Body.STATIC)
    body.position = pos
    line = pymunk.Segment(body, p1, p2, 3)
    line.friction = 1
    line.color = (0, 255, 0, 255)
    space.add(body, line)

def pid1(x):
    y=100*x
    return y

def pid2(x, px=[0, 0]):
    y=10*x+100*px[0]+10*px[1]
    px[1]=px[0]
    px[0]=x
    return y

def pid(x, x0=0, perr=[0], i=[0]):
    dt=0.02
    err=x-x0
    i[0] = i[0] + err * dt*1000
    d=(err-perr[0])/dt
    y=100*err+i[0]+100*d
    perr[0]=err
    if y<-10: y=-10
    if y>10: y=10
    return y

create_static(pos=(0, 10), p1=(-200, 10),p2=(700, 10))
create_static(pos=(0, 10), p1=(0, 10), p2=(0, 1000))
create_static(pos=(700, 10), p1=(0, 10), p2=(0, 1000))
pbody, cbody, cbody2, c, c2, c3 = create_moto()


draw_options = pymunk.pyglet_util.DrawOptions()
#draw_options.shape_static_color=(0,0,0)

def draw(canvas):
    global pbody, cbody, cbody2, c, c2, c3
    background(1)
    if canvas.keys.char=="a":
        cbody.angular_velocity+= 2
        cbody2.angular_velocity+= 2
    if canvas.keys.char=="d":
        cbody.angular_velocity+= -2
        cbody2.angular_velocity+= -2
    if canvas.keys.char=="w":
        pbody._set_angle(0.1)
    if canvas.keys.char=="s":
        pbody._set_angle(-0.1)
    print pbody.angle
    cbody.angular_velocity=cbody2.angular_velocity=pid(pbody.angle)
    space.step(0.02)
    space.debug_draw(draw_options)


#canvas.size = 700, 500
canvas.fullscreen=True
canvas.run(draw)
