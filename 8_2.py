#encoding: utf-8
from __future__ import division

from nodebox.graphics import *
import pymunk
import pymunk.pyglet_util
import random, time
from nodebox.gui import *

def action(arg):
    print panel.field.value
    return

panel = Panel("Example", width=200, height=200)
panel.append(
    Rows(controls=[
                  Field(value="hello world", id="field", action=action),
      (   "size", Slider(default=1.0, min=0.0, max=2.0, steps=100)),
      ("opacity", Slider(default=1.0, min=0.0, max=1.0, steps=100)),
      (  "show?", Checkbox(default=True)),
      Button("Reset", action=lambda button: None)]))
panel.pack()
canvas.append(panel)

space = pymunk.Space()

def create_body(x, y, h, w, r, g, b):
    body = pymunk.Body()
    body.position = x, y
    poly = pymunk.Poly.create_box(body, size=(h, w))
    poly.mass = 1
    poly.friction = 1
    poly.color=(r, g, b, 255)
    space.add(body, poly)
    return body

def create_static(pos=(300, 120), p1=(-200, 0),p2=(300, 0)):
    body = pymunk.Body(body_type = pymunk.Body.STATIC)
    body.position = pos
    line = pymunk.Segment(body, p1, p2, 3)
    line.friction = 1
    line.color = (0, 255, 0, 255)
    space.add(body, line)

body=create_body(x=300, y=300, h=10, w=20, r=255, g=0, b=0)
body2=create_body(100, 100, 30, 30, 0, 255, 0)
body3=create_body(200, 200, 40, 10, 0, 0, 255)

for i in range(100,200):
    create_body(i, i, 10, 10, 0, 255, 0)

create_static(pos=(0, 10), p1=(-200, 10), p2=(700, 10))
create_static(pos=(0, 10), p1=(0, 10), p2=(0, 1000))
create_static(pos=(700, 10), p1=(0, 10), p2=(0, 1000))
create_static(pos=(0, 600), p1=(-200, 10), p2=(700, 10))

draw_options = pymunk.pyglet_util.DrawOptions()
#draw_options.shape_static_color=(0,0,0)
vx,vy=0,0
def draw(canvas):
    global body,vx,vy
    background(1)
    if canvas.mouse.button==LEFT:
        vx, vy=canvas.mouse.x-body.position[0], canvas.mouse.y-body.position[1]
    if canvas.keys.char=="a":
        vx-=10
    if canvas.keys.char=="d":
        vx+=10
    if canvas.keys.char=="w":
        vy+=10
    if canvas.keys.char=="s":
        vy-=10
    body.velocity = vx, vy

    space.step(0.01)
    space.debug_draw(draw_options)

canvas.fullscreen=True
canvas.run(draw)