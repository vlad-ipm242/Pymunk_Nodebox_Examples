#encoding: utf-8
from nodebox.graphics import *
import pymunk
import pymunk.pyglet_util
import time, itertools
import numpy as np

space = pymunk.Space()

body = pymunk.Body()
body.position = 0,40
poly = pymunk.Poly.create_box(body, size=(20,10))
poly.mass = 10
#poly.friction = 1
poly.color = (255, 0, 0, 255)
space.add(body, poly)

def get_intersection(start_point = (0, 0), end_point = (200, 200)):
    query_info = space.segment_query_first(start_point, end_point, 1, pymunk.ShapeFilter())
    #або space.segment_query!!!
    if query_info:
        intersection_point = query_info.point
        return intersection_point
    else:
        return None

draw_options = pymunk.pyglet_util.DrawOptions()

ax=-65
a=0
X=[]
def draw(canvas):
    global ax,a,X
    background(1)
    body._set_angle(a)
    space.step(0.02)
    x=np.sin(np.radians(ax))*100
    stroke(0, 0, 1, 1)
    line(0, 0, x, 100)
    ip=get_intersection(start_point = (0, 0), end_point = (x, 100))!=None
    X.append(int(ip))
    print int(ip),
    space.debug_draw(draw_options)
    ax+=13
    if ax>65:
        print
        body._set_position([np.random.randint(-100,100),40])
        ax=-65
        a+=np.radians(10)
        if a>2*np.pi:
            canvas.stop()
            X=np.array(X)
            X=X.reshape((X.size/11,11))

canvas.size = 500, 500
canvas.run(draw)
