#encoding: utf-8
from __future__ import division

from nodebox.graphics import *
import pymunk
import pymunk.pyglet_util
import random
space = pymunk.Space()
space.gravity = 0,-981

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

def create_poly(x,y,x1,y1):
    body = pymunk.Body()
    body.position = x,y
    body.velocity= x1,y1
    poly = pymunk.Poly.create_box(body, size=(random.randint(10,40),10))
    poly.mass = 10
    poly.friction = 1
    poly.color = (255, 0, 0, 255)
    space.add(body, poly)

body2 = pymunk.Body(body_type = pymunk.Body.STATIC)
body2.position = (300, 300)
l1 = pymunk.Segment(body2, (-150, 0), (255, 0), 3)
l1.friction = 1
l1.color = (0, 255, 0, 255)
space.add(body2, l1)

draw_options = pymunk.pyglet_util.DrawOptions()
#draw_options.shape_static_color=(0,0,0)

def draw(canvas):
    if canvas.mouse.button==MIDDLE:
        create_poly(0, 0, canvas.mouse.x*2, canvas.mouse.y*2)


    background(1)
    space.step(0.02)
    if canvas.mouse.button==RIGHT:
        x,y=canvas.mouse.x,canvas.mouse.y
        cbody.angular_velocity= -(x-250)/10
        cbody2.angular_velocity= -(x-250)/10
    space.debug_draw(draw_options)


canvas.size = 500, 500
canvas.run(draw)
