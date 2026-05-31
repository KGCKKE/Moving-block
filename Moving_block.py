import pygame as pg
import numpy as np
import sys, math
from pygame.locals import *
import random

pg.init()


fps = 120
SCREEN_WIDTH = 700
SCREEN_HIGHT = 400
SPEED = 3
target_image = "block.png"  ##Please put the image file in the same folder as this code, and name it "block.png". The image should be a square, and its size will determine the size of the moving block.


FramePerSecond = pg.time.Clock()
DISPLAYSURF = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HIGHT))
DISPLAYSURF.fill((0, 0, 0))
pg.display.set_caption("114514")

class block(pg.sprite.Sprite):
    def __init__(self):
            super().__init__()
            self.image = pg.image.load(target_image)
            self.rect = self.image.get_rect()
            self.hf_height = self.image.get_height() / 2
            self.hf_width = self.image.get_width() / 2

            self.ran_center = (float(random.randint(0, SCREEN_HIGHT)), float(random.randint(0, SCREEN_WIDTH)))
            self.rect.center = self.ran_center

            self.act_center = np.array(self.ran_center)
            self.vir_center = np.array(self.ran_center)
            self.block_edge = np.array([[-self.hf_width, -self.hf_height], [self.hf_width, self.hf_height]]) + self.act_center #topleft(x, y), bottomright(x, y)
            self.direction = random.randint(-180, 179) / 180 # in 1 pi radian

    def update_actvalue(self):
        To = self.block_edge[0,1] < 0
        Le = self.block_edge[0,0] < 0
        Ri = self.block_edge[1,0] > SCREEN_WIDTH
        Bo = self.block_edge[1,1] > SCREEN_HIGHT

        if (To or Bo) and (Le or Ri):
            self.direction += 1
            if To and Le:
                self.act_center = np.array([self.hf_width, self.hf_height])
            elif To and Ri:
                self.act_center = np.array([SCREEN_WIDTH - self.hf_width, self.hf_height])
            elif Bo and Le:
                self.act_center = np.array([self.hf_width, SCREEN_HIGHT - self.hf_height])
            elif Bo and Ri:
                self.act_center = np.array([SCREEN_WIDTH - self.hf_width, SCREEN_HIGHT - self.hf_height])
        elif To or Bo:
            self.direction = -self.direction
            if To:
                self.act_center[1] = self.hf_height
            else:
                self.act_center[1] = SCREEN_HIGHT - self.hf_height
        elif Le or Ri:
            self.direction = 1 - self.direction
            if Le:
                self.act_center[0] = self.hf_width
            else:
                self.act_center[0] = SCREEN_WIDTH - self.hf_width

        while self.direction < -1:
             self.direction += 2
        while self.direction >= 1:
             self.direction -= 2

        move = np.array([math.cos(math.pi * self.direction) * SPEED, math.sin(math.pi * self.direction)* SPEED])
        self.act_center += move
        self.block_edge = np.array([[-self.hf_width, -self.hf_height], [self.hf_width, self.hf_height]]) + self.act_center #topleft(x, y), bottomright(x, y)

    def update_virvalue(self):
         self.vir_center = np.round(self.act_center).astype(int)
         self.rect.center = (self.vir_center[0], self.vir_center[1])

    def draw(self, surface):
        surface.blit(self.image, self.rect)

B1 = block()

while True:
    for event in pg.event.get():              
        if event.type == QUIT:
            pg.quit()
            sys.exit()

    B1.update_actvalue()
    B1.update_virvalue()
     
    DISPLAYSURF.fill((0, 0, 0))
    B1.draw(DISPLAYSURF)
    pg.display.update()
    FramePerSecond.tick(fps)