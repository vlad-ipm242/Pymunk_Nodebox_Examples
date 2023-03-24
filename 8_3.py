#encoding: utf-8
"""Увага! Англійська клавіатура"""
from __future__ import division

from nodebox.graphics import *
import pymunk
import pymunk.pyglet_util
import random, time
space = pymunk.Space()

body = pymunk.Body()
body.position = 300, 300
poly = pymunk.Poly(body, ((0,20),(0,30),(30,40),(30,10)))
#poly = pymunk.Poly.create_box(body, size=(40, 20))
poly.mass = 1
poly.friction = 1
space.add(body, poly)

cbody = pymunk.Body()
cbody.position = 300, 200
cshape = pymunk.Circle(cbody, 10, (0,0))
cshape.mass=1
space.add(cbody, cshape)

cbody2 = pymunk.Body()
cbody2.position = 200, 200
#cbody.update_velocity(cbody, (0.,0.), 0.9, 0.02)
cshape2 = pymunk.Circle(cbody2, 10, (0,0))
cshape2.mass=1
cshape2.color = (255, 0, 0, 255)
space.add(cbody2, cshape2)

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
        body.angle-=0.1
    if canvas.keys.char=="d":
        body.angle+=0.1
    if canvas.keys.char=="w":
        body.position=body.position[0]+cos(body.angle), body.position[1]+sin(body.angle)

    body.velocity=body.velocity[0]*0.9, body.velocity[1]*0.9
    #cbody.velocity=cbody.velocity[0]*0.9, cbody.velocity[1]*0.9
    space.step(0.02)
    space.debug_draw(draw_options)

canvas.size = 700, 500
canvas.run(draw)