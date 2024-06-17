# -*- coding: utf-8 -*-
"""
Created on Wed May 22 16:13:28 2024

@author: Lenovo
"""

import pygame
import sys
from pygame.locals import QUIT
from const import *
from game import *

#初始化所有模块，image，display等，返回成功的值与失败的值
pygame.init()

DS = pygame.display.set_mode(Game_SIZE)
#image = pygame.image.load(os.path.relpath('pic/other/back.png','pz'))
#第一个参数是相对路径，第二个参数是基准路径
game=Game(DS)

#游戏主循环
while True:
    #监听事件
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type==pygame.MOUSEBUTTONDOWN:
            game.mouseClickHandler(event.button)
    game.update()
    DS.fill((255,255,0))#RGB背景颜色
    game.draw()
    pygame.display.update()
    