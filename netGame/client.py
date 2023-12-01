# -*- coding: utf-8 -*-
from tools import send, inSector, math

class Robot(object):
    u"Робот учасника змагань"
    def __init__(self, shapeName):
        u"shapeName - назва об'єкта на сервері. Повідомляє організатор"
        self.s=shapeName
    def setangle(self, a):
        u"установити кут"
        send(self.s+".body.angle=%f"%a)
    def getangle(self):
        u"отримати кут"
        return float(send(self.s+".body.angle"))
    def setvel(self, v):
        u"установити швидкість"
        a=self.getangle()
        x,y=v*math.cos(a), v*math.sin(a)
        self.setvelXY(x,y)
    def setvelXY(self, x, y):
        u"установити вектор швидкості"
        if abs(x)>100 or abs(y)>100: return
        send(self.s+".body.velocity=%i,%i"%(x,y))
    def setangvel(self, w):
        u"установити кутову швидкість"
        if abs(w)>100: return
        send(self.s+".body.angular_velocity=%i"%w)
    def getpos(self,s=""):
        u"отримати координати"
        if s=="": s=self.s
        x=send(s+".body.position")
        return [float(i) for i in x[6:-1].split(", ")]
    def insector(self):
        cx,cy=self.getpos()
        x,y=self.getpos("s0")
        a=self.getangle()
        return inSector(x,y,cx,cy,100.0,a)

b=Robot("s1")