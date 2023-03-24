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
poly = pymunk.Poly.create_box(body, size=(10, 20))
poly.mass = 1
poly.friction = 1
space.add(body, poly)

draw_options = pymunk.pyglet_util.DrawOptions()
#draw_options.shape_static_color=(0,0,0)
vx,vy=0,0
def draw(canvas):
    global body,vx,vy
    background(1)
    if canvas.keys.char=="a":
        vx-=10
    if canvas.keys.char=="d":
        vx+=10
    if canvas.keys.char=="w":
        vy+=10
    if canvas.keys.char=="s":
        vy-=10
    vx*=0.9
    vy*=0.9
    body.velocity = vx, vy
    #body.position = vx, vy

    space.step(0.02)
    space.debug_draw(draw_options)

canvas.size = 700, 500
canvas.run(draw)