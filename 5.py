#encoding: utf-8
from __future__ import division

from nodebox.graphics import *
import pymunk
import pymunk.pyglet_util
import random, time
space = pymunk.Space()
space.gravity = 0,-981

def create_moto(x1=20, x2=20):
    cbody = pymunk.Body()
    cbody.position = 0,100
    circle=pymunk.Circle(cbody, x1)
    circle.mass = 100
    circle.friction = 1
    space.add(cbody, circle)
    cbody2 = pymunk.Body()
    cbody2.position = 100,100
    circle2=pymunk.Circle(cbody2, x2)
    circle2.mass = 100
    circle2.friction = 1
    c = pymunk.PinJoint(cbody, cbody2, (0, 0), (0, 0))
    space.add(cbody2, circle2, c)
    pbody = pymunk.Body()
    pbody.position = 50,150
    poly = pymunk.Poly.create_box(pbody, size=(50,20))
    poly.mass = 10
    poly.friction = 1
    c2 = pymunk.PinJoint(cbody, pbody, (0, 0), (0, 0))
    c3 = pymunk.DampedSpring(cbody2, pbody, (0, 0), (0, 0), 50, 5000, 300)
    space.add(pbody, poly, c2, c3)
    return pbody, cbody, cbody2, c, c2, c3



def create_poly(x,y,x1,y1):
    body = pymunk.Body()
    body.position = x,y
    body.velocity= x1,y1
    poly = pymunk.Poly.create_box(body, size=(random.randint(10,40),10))
    poly.mass = 10
    poly.friction = 1
    poly.color = (255, 0, 0, 255)
    space.add(body, poly)

def create_static(pos=(300, 100), p1=(-200, 0),p2=(300, 0)):
    body = pymunk.Body(body_type = pymunk.Body.STATIC)
    body.position = pos
    line = pymunk.Segment(body, p1, p2, 3)
    line.friction = 1
    line.color = (0, 255, 0, 255)
    space.add(body, line)


create_static(pos=(0, 10), p1=(-200, 10),p2=(700, 10))
pbody, cbody, cbody2, c, c2, c3 = create_moto()

for i in range(50):
    create_poly(random.randint(300,400), 200, 0, 0)

draw_options = pymunk.pyglet_util.DrawOptions()
#draw_options.shape_static_color=(0,0,0)
tm=0
x1=10
x2=10
def draw(canvas):
    global pbody, cbody, cbody2, c, c2, c3, tm, space, x1, x2
    background(1)
    print tm
    if tm>10 or cbody2.position[0]>600 or canvas.keys.char=="a":
        space = pymunk.Space()
        space.gravity = 0,-981
        create_static(pos=(0, 10), p1=(-200, 10),p2=(700, 10))
        for i in range(50):
            create_poly(random.randint(300,400), 200, 0, 0)
        # for i in pbody, cbody, cbody2, c, c2, c3:
        #     i.position=1000,1000
        #     space.remove(i)
        pbody, cbody, cbody2, c, c2, c3 = create_moto(x1,x2)
        tm=0
        if x1==40:
            x1=10
            x2+=1
        x1+=1

    space.step(0.05)
    tm+=0.05
    cbody.angular_velocity= -5
    cbody2.angular_velocity= -5
    pbody.angular_velocity= -5
    space.debug_draw(draw_options)


canvas.size = 700, 500
canvas.run(draw)
