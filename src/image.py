# -*- coding: utf-8 -*-

import pygame
import os

class Image(pygame.sprite.Sprite): #sprite是所有游戏对象的基类
    def __init__(self,pathFmx,pathIndex,pos,size=None,pathIndexcount=0):
        self.pos=list(pos) #将传入的元组强转为列表
        self.pathIndexcount=pathIndexcount #对象有几张图片，决定 是否要对路径进行格式化，只有一张图片的路径没有格式化字符串
        self.pathIndex=pathIndex
        self.size=size
        self.pathFmx=os.path.relpath(pathFmx,'pz') #第一个参数是 相对路径，第二个参数是 基准路径
        self.updateImage()
        
#每一次update信息都要调用updateimage，是因为需要得到新的self.image对象
    
    def updateImage(self):
        path=self.pathFmx
        if self.pathIndexcount != 0: #对象有几张图片，决定 是否要对路径进行格式化，只有一张图片的路径没有格式化字符串
            path=path % self.pathIndex #格式化得到真正的图片路径
        self.image=pygame.image.load(path)
        #若指定了大小，则进行缩放
        if self.size:
            self.image=pygame.transform.scale(self.image, self.size)#该方法返回一个 新的对象，故进行赋值处理
        
    def updateSize(self,size):
        self.size=size #更新大小之后，更新图片，否则self.image没更新，现实的还是原来的
        self.updateImage()
    
    def updateIndex(self,pathIndex):
        self.pathIndex=pathIndex #更新图片索引，从而在updateimage中得到下一张图片的路径
        self.updateImage()
    
    def getRect(self):
        rect=self.image.get_rect() #获取image左上角坐标与image大小
        rect.x,rect.y=self.pos #左上角的坐标，如果不更新，则其默认为左上角(0,0)
        return rect
    
    def doLeft(self):
        pass
    
    def draw(self,ds):
        ds.blit(self.image,self.getRect()) #self.image实际上是一个surface对象，使用这个方法黏贴到主框上去