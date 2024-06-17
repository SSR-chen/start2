# -*- coding: utf-8 -*-
import image
import time
import Data_object

class ObjectBase(image.Image):
    def __init__(self,id,pos):
        self.id=id
        self.preIndexTime=0
        self.prePositionTime=0
        self.preSummonTime=0
        self.hp=self.getData()['HP']
        self.attack=self.getData()['ATT']
        #调用父类中的初始化方法
        super(ObjectBase,self).__init__(self.getData()['PATH'],
                                        0,
                                        pos,
                                        self.getData()['SIZE'],
                                        self.getData()['IMAGE_INDEX_MAX'])
    
    def getData(self):
        return Data_object.data[self.id]
    
    def getPositionCD(self):
        return self.getData()['POSITION_CD']
    
    def getImageIndexCD(self):
        return self.getData()['IMAGE_INDEX_CD']
    
    def getSummonCD(self):
        return self.getData()['SUMMON_CD']
        
    def getSpeed(self):
        return self.getData()['SPEED']
    
    def getPrice(self):
        return self.getData()['PRICE']
    
    def isCollide(self,other):
        return self.getRect().colliderect(other.getRect())
    
    def canLoot(self):
        return self.getData()['CAN_LOOT']
    
    def update(self):
        self.checkImageIndex()
        self.checkPosition()
        self.checkSummon()
        
    def checkSummon(self):
        if time.time()-self.preSummonTime<=self.getSummonCD():
            return 
        self.preSummonTime=time.time()
        self.preSummon()
        
    def checkImageIndex(self):
        if time.time()-self.preIndexTime<=self.getImageIndexCD():
            return
        self.preIndexTime=time.time()
        idx=self.pathIndex+1#图片切换到下一帧
        if idx>=self.pathIndexcount:
            idx=0
        self.updateIndex(idx)
    
    def checkPosition(self):
        if time.time()-self.prePositionTime<=self.getPositionCD():
            return False
        speed=self.getSpeed()
        self.pos=(self.pos[0]+speed[0],self.pos[1]+speed[1])
        self.prePositionTime=time.time()
        return True
    
    def preSummon(self):
        pass
    
    def hasSummon(self):
        pass
    
    def doSummon(self):
        pass
    
    
    