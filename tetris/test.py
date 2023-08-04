import pygame
import data
import random
import sys
pygame.init()
clock = pygame.time.Clock()
S_H = 20
S_W = 10
B_S = 30
ts = 27
screen = pygame.display.set_mode((S_W*B_S,S_H*B_S))
screen.fill((0,0,0))
class Block(pygame.sprite.Sprite):
    def __init__(self,px,py,color):
        super().__init__()
        self.image = pygame.Surface([ts,ts])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = [px,py]
    def update(self,dir):
        if not dir:
            return
        if dir == "l":
            self.rect.center= [self.rect.center[0]-B_S,self.rect.center[1]]
        if dir == "r":
            self.rect.center= [self.rect.center[0]+B_S,self.rect.center[1]]
def drawShape(grp,shape,px,py):
    b = data.blocks[shape][0]
    t = px
    for i in b:
        px = t
        for j in i:
            if j == 1:
                b = Block(px,py,(255,0,0))
                grp.add(b)
            px+=B_S
        py+=B_S
shape = pygame.sprite.Group()
drawShape(shape,random.choices(list(data.blocks.keys()))[0],50,50)
blo = shape.sprites()

while True:
    d = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                d = "l"
            if event.key == pygame.K_RIGHT:
                d = "r"
    pygame.display.flip()
    screen.fill((0,0,0))
    shape.draw(screen)
    shape.update(d)
    for i in blo:
        tl,bl,tr,br = i.rect.topleft,i.rect.bottomleft,i.rect.topright,i.rect.bottomright

        pygame.draw.rect(screen,(255,255,255),(tl[0],tl[1],5,5))
        pygame.draw.rect(screen,(255,255,255),(bl[0],bl[1],5,5))
        pygame.draw.rect(screen,(255,255,255),(tr[0],tr[1],5,5))
        pygame.draw.rect(screen,(255,255,255),(br[0],br[1],5,5))
    clock.tick(60)

