# -*- coding: utf-8 -*-

import object_base
import sunlight
class SunFlower(object_base.ObjectBase):
    def __init__(self, id, pos):
        super(SunFlower, self).__init__(id, pos)
        self.hasSunlight=False #这个常量代表此时要不要召唤
        
    def preSummon(self):
        self.hasSunlight=True        
        
    def hasSummon(self):
        return self.hasSunlight
    
    def doSummon(self):
        if self.hasSummon():     
            self.hasSunlight=False
            return sunlight.SunLight(2,(self.pos[0]+20,self.pos[1]-10))
        
