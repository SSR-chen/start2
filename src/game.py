# -*- coding: utf-8 -*-

import time
import image
import sun_flower
import pygame
import pean_shooter
import zombie_base
import random
from const import *
import Data_object

class Game(object):
    def __init__(self,ds):
        self.ds=ds
        self.back=image.Image(PATH_BACK,0,(0,0),Game_SIZE,0)
        self.lose=image.Image(PATH_LOSE,0,(0,0),Game_SIZE,0)
        self.isGameOver=False
        self.plants=[]
        self.zombies=[]
        self.summons=[]
        self.hasPlant=[]
        self.gold=100
        self.goldPoint=pygame.font.Font(None,60)
        
        self.zombie=0
        self.zombieFont=pygame.font.Font(None,60)
        
        self.zombieGenerateTime=0
        for i in range(GRID_SIZE[0]):
            col=[]
            for j in range(GRID_SIZE[1]):
                col.append(0)
            self.hasPlant.append(col)
        
    
    #转换单位，像素点转为格子数
    def getIndexByPos(self,pos):
        x=(pos[0]-LEFT_TOP[0])//GRID_SIZE[0]
        y=(pos[1]-LEFT_TOP[1])//GRID_SIZE[1]
        return x,y
    
    def renderFont(self):
        textImage=self.goldPoint.render('Gold:'+str(self.gold),True,(0,0,0))
        self.ds.blit(textImage,(13,23))
        textImage=self.goldPoint.render('Gold:'+str(self.gold),True,(255,255,255))
        self.ds.blit(textImage,(10,23))
        
        textImage=self.zombieFont.render('Score:'+str(self.zombie),True,(0,0,0))
        self.ds.blit(textImage,(13,83))
        textImage=self.zombieFont.render('Score:'+str(self.zombie),True,(255,255,255))
        self.ds.blit(textImage,(10,83))
    
    def draw(self):
        self.back.draw(self.ds)
        for plant in self.plants:
            plant.draw(self.ds)
        for summon in self.summons:
            summon.draw(self.ds)
        for zombie in self.zombies:
            zombie.draw(self.ds)
        self.renderFont()    
        if self.isGameOver:
            self.lose.draw(self.ds)
            
    def update(self):
        #print('gold:',self.gold)
        self.back.update()
        for plant in self.plants:
            plant.update()
            if plant.hasSummon():
                summ=plant.doSummon()
                self.summons.append(summ)
        for summon in self.summons:
            summon.update()
        for zombie in self.zombies:
            zombie.update()
        #僵尸出生时间间隔
        if time.time()-self.zombieGenerateTime>ZOMBIE_BORN_CD:
            self.zombieGenerateTime=time.time()
            self.addZombie(ZOMBIE_BORN_x,
                           
                           random.randint(0,GRID_COUNT[1]-1))
        self.checkSummonVSZombie()
        self.checkZombieVSPlants()
        
        for zombie in self.zombies:
            if zombie.getRect().x<=0:
                self.isGameOver=True
                
        
        #防止内存泄漏
        for summon in self.summons:
            if summon.getRect().x>Game_SIZE[0] or summon.getRect().y>Game_SIZE[1]:
                self.summons.remove(summon)
                break
    
    def checkZombieVSPlants(self):
        for zombie in self.zombies:
            for plant in self.plants:
                if zombie.isCollide(plant):
                    self.fight(zombie,plant)
                    if plant.hp<=0:
                        self.plants.remove(plant)
                        break
    
    
    def checkSummonVSZombie(self):
        for summon in self.summons:
            for zombie in self.zombies:
                if summon.isCollide(zombie): #碰撞检测
                    self.fight(summon,zombie)
                    if zombie.hp<=0:
                        self.zombies.remove(zombie)
                        self.zombie+=1
                    if summon.hp<=0:
                        self.summons.remove(summon)
                    return   
    
    def addFlower(self,x,y):
        pos=(LEFT_TOP[0]+x*GRID_SIZE[0],y*GRID_SIZE[1]+LEFT_TOP[1])
        sf=sun_flower.SunFlower(3,pos)
        self.plants.append(sf)
    
    def addPeanShooter(self,x,y):
        pos=(LEFT_TOP[0]+x*GRID_SIZE[0],y*GRID_SIZE[1]+LEFT_TOP[1])
        ps=pean_shooter.PeanShooter(PEANSHOOTER_ID,pos)
        self.plants.append(ps)
    
    def addZombie(self,x,y):
        pos=(LEFT_TOP[0]+x*GRID_SIZE[0],y*GRID_SIZE[1]+LEFT_TOP[1])
        zm=zombie_base.ZombieBase(1, pos)
        self.zombies.append(zm)
    
    def fight(self,a,b):
        while True:
            a.hp-=b.attack
            b.hp-=a.attack
            if b.hp<=0:
                return True
            if a.hp<=0:
                return False
        return False
            
    def checkLoot(self,mousePos):
        for summon in self.summons:
            if not summon.canLoot():
                continue
            rect=summon.getRect()
            if rect.collidepoint(mousePos):
                self.summons.remove(summon)
                self.gold+=summon.getPrice()
                return True
            return False
    
    def checkAddplant(self,mousePos,objId):
        x,y=self.getIndexByPos(mousePos)
        #注意这几个return，一旦有一个不满足就终止，所以要放在一起！！！它们对于结果的影响是十分重要的
        if x<0 or x>=GRID_COUNT[0]:
            return
        if y<0 or y>=GRID_COUNT[1]:
            return
        if self.gold<Data_object.data[objId]['PRICE']:
            return
        if self.hasPlant[x][y]==1:
            return
        self.hasPlant[x][y]=1
        self.gold-=Data_object.data[objId]['PRICE']
        if objId==SUNFLOWER_ID:
            self.addFlower(x,y) #这里的x，y单位是格子数
        elif objId==PEANSHOOTER_ID:
            self.addPeanShooter(x, y)
        
    def mouseClickHandler(self,btn):
        if self.isGameOver:
            return
        mousePos=pygame.mouse.get_pos()
        self.checkLoot(mousePos) #Loot就是捡的意思
        if self.checkLoot(mousePos):
            return
        if btn==1:
            self.checkAddplant(mousePos,SUNFLOWER_ID)
        elif btn==3:
            self.checkAddplant(mousePos, PEANSHOOTER_ID)