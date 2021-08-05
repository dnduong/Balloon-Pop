import numpy as np
import cv2 
import mediapipe as mp
import math
import random

class Balloon:
    
    def __init__(self,w,h,v,r,c):
        self.w = w
        self.h = h
        self.x = random.randint(r, int(w) - r)
        self.y = int(h)
        self.velocity = v
        self.radius = r
        self.color = c
        self.nb_pieces = 8
        
    def draw(self,panel):
        cv2.circle(panel,(self.x,self.y),self.radius,self.color,-1)
        triangle_cnt = np.array([(self.x,self.y+int(self.radius/2)),
                                (self.x-int(self.radius/4),self.y+int(self.radius/3*4)),
                                (self.x+int(self.radius/4),self.y+int(self.radius/3*4))])
        cv2.line(panel, (self.x,self.y+int(self.radius/3*4)),(self.x,self.y+int(self.radius*3)), 
                (255,255,255), 2)
        cv2.drawContours(panel, [triangle_cnt], 0, self.color, -1)
        cv2.circle(panel,(self.x-int(self.radius/4),self.y-int(self.radius/4)),int(self.radius/4),(255,255,255),-1)
  

    def move(self):
        self.y = self.y - self.velocity

    def touch(self,fingers,r):
        for p in fingers:
            if p != None :
                if math.dist((self.x,self.y),p) < r + self.radius : return True
        return False
    
    def respawn(self):
        self.x = random.randint(self.radius, int(self.w) - self.radius)
        self.y = int(self.h)