# -*- coding: utf-8 -*-

import object_base
import pean_bullet
import time

class PeanShooter(object_base.ObjectBase):
    def __init__(self, id, pos):
        super(PeanShooter, self).__init__(id, pos)
        self.hasShoot=False
        self.hasBullet=False #这个常量代表此时要不要召唤
        
    def preSummon(self):
        self.hasShoot=True   
        self.pathIndex=0
        
    def hasSummon(self):
        return self.hasBullet
    
    def doSummon(self):
        if self.hasSummon():     
            self.hasBullet=False
            return pean_bullet.PeanBullet(0,
                                          (self.pos[0]+100,self.pos[1]+40))
        
    def checkImageIndex(self):
        if time.time()-self.preIndexTime<=self.getImageIndexCD():
            return
        self.preIndexTime=time.time()
        idx=self.pathIndex+1#图片切换到下一帧
        if idx==8 and self.hasShoot:
            self.hasBullet=True
        if idx>=self.pathIndexcount:
            idx=9
        self.updateIndex(idx)