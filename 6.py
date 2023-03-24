#encoding: utf-8
from __future__ import division
from nodebox.graphics import *
import pymunk
import pymunk.pyglet_util

space = pymunk.Space()
space.gravity = 0, -981

def add_body(x, y, h, w, body_type=pymunk.Body.DYNAMIC):
    body = pymunk.Body(body_type =body_type)
    body.position = x, y
    shape = pymunk.Segment(body, (0,0), (h,w), 5)
    shape.friction = 1.0
    shape.color=(255, 0, 0, 255)
    if not body_type==pymunk.Body.STATIC:
        shape.mass = 10
    space.add(body, shape)
    return body

b0 = add_body(-100, 100, 1000, 0, pymunk.Body.STATIC)
b1 = add_body(300, 110, 50, 0)
b2 = add_body(300, 110, 0, 50)
c=pymunk.PivotJoint(b1, b2, (300, 25))
space.add(c)


draw_options = pymunk.pyglet_util.DrawOptions()
#draw_options.shape_static_color=(0,0,0)

def draw(canvas):
    #if canvas.mouse.button==LEFT:
    #    b1.angular_velocity=canvas.mouse.x-250 #, canvas.mouse.y-250

    background(1)
    space.step(0.002)
    space.debug_draw(draw_options)


canvas.size = 500, 500
canvas.run(draw)
