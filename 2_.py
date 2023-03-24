#encoding: utf-8
from __future__ import division
#import pyglet
from nodebox.graphics import *
import pymunk
import pymunk.pyglet_util

space = pymunk.Space()
space.gravity = 0,-981

def createBody():
    body = pymunk.Body()
    poly = pymunk.Poly.create_box(body, size=(30,10))
    poly.mass = 10
    poly.friction = 1
    poly.color = (255, 0, 0, 255)
    space.add(body, poly)
    return body

def createStatic(x,y):
    body = pymunk.Body(body_type = pymunk.Body.STATIC)
    body.position = x,y
    l = pymunk.Segment(body, (0, 0), (100, 0), 3)
    l.friction = 1
    l.color = (0, 255, 0, 255)
    space.add(body, l)
    return body

draw_options = pymunk.pyglet_util.DrawOptions()
#draw_options.shape_static_color=(0,0,0)

def draw(canvas):
    if canvas.mouse.button==LEFT:
        body=createBody()
        body.position=0,0
        body.velocity=canvas.mouse.x*2, canvas.mouse.y*2
    if canvas.mouse.button==RIGHT:
        createStatic(canvas.mouse.x, canvas.mouse.y)

    background(1)
    space.step(0.02)
    #x,y=body.position.x,body.position.y
    #fill(0,0,0)
    #ellipse(x,y,10,10)
    space.debug_draw(draw_options)


canvas.size = 500, 500
canvas.run(draw)
