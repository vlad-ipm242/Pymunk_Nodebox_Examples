# -*- coding: utf-8 -*-
import thread
import socket
from tools import *

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 50007))
s.listen(5)

def f(C):
    while 1:
        soc, addr = s.accept()
        x=soc.recv(255)
        print x
        C.append(x)
        try:
            x=str(eval(x))
        except:
            pass
        soc.sendall(x)
        soc.close()

C=[""]
thread.start_new(f, (C,))
draw_options = pymunk.pyglet_util.DrawOptions()

def draw(canvas):
    canvas.clear()
    fill(0,0,0,1)
    text("%i"%canvas.frame,20,20)
    try:
        #exec "\n".join(C)
        exec C.pop()
    except:
        pass
    nofill()
    ellipse(350, 250, 350, 350, stroke=Color(0))
    simFriction()
    space.step(0.02)
    space.debug_draw(draw_options)

canvas.size = 700, 500
canvas.run(draw)
