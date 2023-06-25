#encoding: utf-8
from __future__ import division

from nodebox.graphics import *
import pymunk
import pymunk.pyglet_util
import random, time

def create_moto(x):
    """Створює візок. Індекси списку параметрів x:
    0 - радіус заднього колеса
    1 - радіус переднього колеса
    2 - відстань між колесами (мінімальна)
    3 - виліт заднього колеса
    4 - виліт переднього колеса
    """
    y0=100 # висота осей над землею
    l=x[0]+x[1]+x[2] # відстань між осями
    b0 = pymunk.Body() # заднє колесо
    b0.position = 0-x[3],y0
    g0=pymunk.Circle(b0, x[0])
    g0.mass = 100
    g0.friction = 1

    b1 = pymunk.Body() # переднє колесо
    b1.position = l+x[4],y0
    g1=pymunk.Circle(b1, x[1])
    g1.mass = 100
    g1.friction = 1

    b2 = pymunk.Body() # корпус
    b2.position = l/2,y0+max([x[0],x[1]])+15
    g2 = pymunk.Poly.create_box(b2, size=(l,20))
    g2.mass = 100
    g2.friction = 0

    # з'єднання:
    J=(
    pymunk.PinJoint(b0, b2, (0, 0), (0, 0)),
    pymunk.PinJoint(b1, b2, (0, 0), (0, 0)),
    pymunk.PinJoint(b0, b2, (0, 0), (-l/2, 0)),
    pymunk.PinJoint(b1, b2, (0, 0), (l/2, 0)))
    # pymunk.DampedSpring(b0, b2, (0, 0), (0, 0), 50, 50000, 300),
    # pymunk.DampedSpring(b1, b2, (0, 0), (0, 0), 50, 50000, 300),
    # pymunk.DampedSpring(b0, b2, (0, 0), (-40, 0), 50, 50000, 300),
    # pymunk.DampedSpring(b1, b2, (0, 0), (40, 0), 50, 50000, 300)
    # )
    #J[0].distance=60
    #J[1].distance=60

    space.add(b0, b1, b2, g0, g1, g2, *J) # додати в space
    return (b0, b1, b2, g0, g1, g2)+J

def create_poly(x,y,x1,y1):
    """Створює випакову цеглину з позицією x,y і швидкістю x1,y1"""
    body = pymunk.Body()
    body.position = x,y
    body.velocity= x1,y1
    poly = pymunk.Poly.create_box(body, size=(random.randint(10,40),10))
    poly.mass = 10
    poly.friction = 1
    poly.color = (255, 0, 0, 255) # червоний колір (R,G,B,A)
    space.add(body, poly)

def create_static(pos=(300, 100), p1=(-200, 0), p2=(300, 0)):
    """Створює нерухоме тіло - лінію за точками p1, p2"""
    body = pymunk.Body(body_type = pymunk.Body.STATIC)
    body.position = pos
    line = pymunk.Segment(body, p1, p2, 3)
    line.friction = 1
    line.color = (0, 255, 0, 255)
    space.add(body, line)


draw_options = pymunk.pyglet_util.DrawOptions()

def draw(canvas):
    """Функція пакету nodebox, що рисує кожен кадр анімації"""
    global tm, space, B # глобальні змінні
    background(1) # зарисувати попередній кадр
    print tm
    if tm>10 or B[1].position[0]>600 or canvas.keys.char=="a":
        canvas.stop()

    space.step(0.05) # симуляція фізики
    tm+=0.05 # збільшити
    B[0].angular_velocity= -5 # швидкість колеса
    B[1].angular_velocity= -5
    space.debug_draw(draw_options) # рисувати усі об'єкти


canvas.size = 700, 500 # розміри вікна
def f(x):
    """Функція, що мінімізується. Повертає час tm, за який візок з параметрами x подолав перешкоду"""
    global tm, space, draw, canvas, B # глобальні змінні
    canvas=Canvas()
    tm=0
    space = pymunk.Space() # створити простір
    space.gravity = 0,-981 # гравітацію
    create_static(pos=(0, 10), p1=(-200, 10), p2=(700, 10)) # дорогу
    for i in range(50):
        create_poly(random.randint(300,400), 200, 0, 0) # цеглини

    B = create_moto(x) # візок з параметрами x
    canvas.run(draw) # розпочати анамацію

    for obj in B:
        obj.position=1000,1000
        space.remove(obj) # видалити усі об'єкти
    return tm

def opti_grid(X=range(0,20)):
    """Функція для оптимізації однієї змінної сітковим методом. Використовується для дослідження впливу обраного параметра на tm"""
    Y=[] # значення часу tm
    for x in X:
        y=[f([30,30,20,14.4,x]) for i in range(3)] # симуляція 3 рази
        Y.append(sum(y)/len(y)) # додати середній час
    plt.plot(X,Y,'o-') # нарисувати графік
    plt.xlabel(u"x, мм"); plt.ylabel(u"t, c")
    plt.show()


import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize, differential_evolution
f([30,30,20,14.4,18.9])
#opti_grid()
#print minimize(f, x0=[25., 25, 17, 10, 10], method="L-BFGS-B", bounds=[(20, 30),(20, 30),(5, 30),(0, 20),(0, 20)])
#print differential_evolution(f, bounds=[(20, 30),(20, 30),(5, 30),(0, 20),(0, 20)], maxiter=10) # знайти мінімум

"""
      fun: 10.050000000000008
 hess_inv: <5x5 LbfgsInvHessProduct with dtype=float64>
      jac: array([        0.        , -10000000.00000014,         0.        ,
               0.        ,         0.        ])
  message: 'ABNORMAL_TERMINATION_IN_LNSRCH'
     nfev: 126
      nit: 0
   status: 2
  success: False
        x: array([25., 25., 17., 10., 10.])

     fun: 5.14999999999999
 message: 'Maximum number of iterations has been exceeded.'
    nfev: 576
     nit: 5
 success: False
       x: array([29.36213895, 29.63160881, 16.96322646, 18.93280667,  5.49028507])

     fun: 5.249999999999989
 message: 'Maximum number of iterations has been exceeded.'
    nfev: 981
     nit: 10
 success: False
       x: array([29.66240257, 29.94598132, 20.04745796, 14.4104782 , 18.85834041])
"""