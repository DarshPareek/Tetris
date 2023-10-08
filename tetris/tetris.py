import pygame
import settings 
from data import blocks
import random
import sys
def bye(score):
    pygame.mixer.music.pause()
    pygame.mixer.init()
    pygame.mixer.music.load("song2.mp3")
    pygame.mixer.music.set_volume(0.7)
    pygame.mixer.music.play()
    while True:
        screen = pygame.display.get_surface()
        screen.fill((49, 49, 49))
        font = pygame.font.Font("Tetris.ttf", 77)
        txtsurf = font.render("YOU LOST", False,(255,255,255))
        screen.blit(txtsurf,(30, 150))
        txtsurf = font.render("SCORE : "+str(score*10), False,(255,255,255))
        screen.blit(txtsurf,(30, 250))
        txtsurf = font.render("DARSH", False,(255,255,255))
        screen.blit(txtsurf,(30, 350))
        txtsurf = font.render("BETTER", False,(255,255,255))
        screen.blit(txtsurf,(30, 450))
        pygame.display.update()
        pygame.time.wait(300000)
        break
    sys.exit()
def randomize():
    c = ["1","2","3"]
    ch = random.choice(c)
    return "Block"+ch+".png"
def drawGrid(sc):
    for i in range(11):
        pygame.draw.line(sc,settings.lbgc,(i*settings.blockSize,0),(i*settings.blockSize,600),2)
    for i in range(21):
        pygame.draw.line(sc,settings.lbgc,(0,i*settings.blockSize),(300,i*settings.blockSize),2)
class Game:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode(settings.ssm)
        self.screen.fill(settings.sbgc)
        self.board = Board(self.screen)
        self.score = 0
        pygame.mixer.init()
        pygame.mixer.music.load("song1.mp3")
        pygame.mixer.music.set_volume(0.7)
        pygame.mixer.music.play()
    def update(self):
        self.screen.fill(settings.sbgc) #self.spawnBlock()
        if not self.board.chkDeath():
            return False
        self.board.block.tetris.draw(self.screen)
        #print(self.board.block.next.sprites())
        pygame.draw.rect(self.screen,(97, 54, 89),(310,10*settings.blockSize,180,200))
        pygame.draw.rect(self.screen,(97, 54, 89),(335,17,137,37))
        pygame.draw.rect(self.screen,(97, 54, 89),(350,265,101,34))
        pygame.draw.rect(self.screen,(97, 54, 89),(346,95,121,37))
        pygame.draw.rect(self.screen,(97, 54, 89),(346,147,121,34))
        font = pygame.font.Font("Tetris.ttf", 30)
        txtsurf = font.render("TETRIS", True,(57, 255, 20) )
        self.screen.blit(txtsurf,(340, 20))
        pygame.draw.rect(self.screen,(0,0,0),(335,17,137,37),3)
        #pygame.draw.rect(self.screen,(97, 54, 89),(335,17,137,37))
        pygame.draw.rect(self.screen,(0,0,0),(350,265,101,34),3)
        font = pygame.font.Font("Tetris.ttf", 30)
        txtsurf = font.render("NEXT", True,(57, 255, 20) )
        self.screen.blit(txtsurf,(355, 270))
        txtsurf = font.render("SCORE", True,(57, 255, 20))
        self.screen.blit(txtsurf,(350, 100))
        txtsurf = font.render(str(self.score*10), True,(57, 255, 20) )
        self.screen.blit(txtsurf,(393, 150))
        pygame.draw.rect(self.screen,(0,0,0),(346,95,121,37),3)
        pygame.draw.rect(self.screen,(0,0,0),(346,147,121,34),3)
        pygame.draw.rect(self.screen,(0,0,0),(310,10*settings.blockSize,180,200),3)
        self.board.block.next.draw(self.screen)
        return True
    def spawnBlock(self):
        self.board.block.spawn()
    def rotate(self):
        self.board.block.rotate()
    def chk(self,d):
        self.score += self.board.block.chkmove(d)
    def chkline(self):
        self.score += self.board.line()
class Board:
    def __init__(self,sc) -> None:
        self.board = []
        for i in range(settings.screenHeight):
            self.board.append([0]*settings.screenWidth)
            self.block = Tetris(self)
        self.screen = sc
        self.locked_pos = []
        self.cdata = {}
    def show(self):
        for i in self.board:
            print(i)
        print(self.locked_pos)
    def add(self,x,y):
        self.board[y][x] = 1
        self.locked_pos.append((x,y))
    def fill(self):
        for i,j in self.locked_pos:
            surf = pygame.image.load("Block4.png")
            self.screen.blit(surf,(i*settings.blockSize,j*settings.blockSize,settings.tilesize,settings.tilesize))
            #pygame.draw.rect(self.screen,(255, 100, 127),(i*settings.blockSize,j*settings.blockSize,settings.tilesize,settings.tilesize))
    def line(self):
        self.cdata = {}
        g = []
        s = 0
        for i in self.locked_pos:
            if i[1] not in list(self.cdata.keys()):
                self.cdata[i[1]] = 1
            if i[1] in list(self.cdata.keys()):
                self.cdata[i[1]] += 1
        for i in self.cdata:
            if self.cdata[i] == 11:
                #print("Line")
                s += 1
                self.clLockedPos(i)
                g.append(i)
        for i in g:
            del self.cdata[i]
        return s
    def clLockedPos(self,y):
        self.board.pop(y)
        self.board = [[0]*10] + self.board
        self.locked_pos = []
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 1:
                    self.locked_pos.append((j,i))
    def chkDeath(self):
        for i in self.locked_pos:
            if i[1] == 1:
                return False
        return True
    # def clLockedPos(self,y):
    #     print("clearing",y)
    #     g = []
    #     for i in self.locked_pos:
    #         if y != i[1]:
    #             g.append(i)
    #     self.locked_pos = g
    #     print(self.locked_pos)
class Tetris:
    def __init__(self,board) -> None:
        self.tetris = pygame.sprite.Group()
        self.bdata = []
        self.x = settings.screenWidth//2
        self.y = 1
        self.board = board
        self.alive = True
        self.next = pygame.sprite.Group()
        self.nbt = blocks.index(random.choice(blocks))
        self.nbdata = []
        self.n = randomize()
    def spawn(self):
        self.bt = self.nbt
        self.nbt = blocks.index(random.choice(blocks))
        #print(blocks[self.nbt],blocks[self.bt])
        self.bdata = []
        self.nbdata = []
        self.tetris = pygame.sprite.Group()
        self.next = pygame.sprite.Group()
        self.x = settings.screenWidth//2
        self.y = 1
        self.c = self.n
        self.n = randomize()
        for i in range(4):
            self.nbdata.append(blocks[self.nbt][i])
        self.addnxtBlock(13.5,12)
        for i in range(4):
            self.bdata.append(blocks[self.bt][i])
        self.addBlock(settings.screenWidth//2,1)
    def addnxtBlock(self,sx,sy):
        self.next = pygame.sprite.Group()
        for i in self.nbdata:
            x = (sx + i[0])*settings.blockSize
            y = (sy + i[1])*settings.blockSize
            self.next.add(Block(x,y,self.n))
    def addToGrid(self,x,y):
        self.board.add(x,y)
    def addBlock(self,sx,sy):
        self.tetris = pygame.sprite.Group()
        for i in self.bdata:
            x = (sx + i[0])*settings.blockSize
            y = (sy + i[1])*settings.blockSize
            self.tetris.add(Block(x,y,self.c))
    def rotate(self):
        self.tetris = pygame.sprite.Group()
        for i in range(4):
            x = self.bdata[i][0]
            y = self.bdata[i][1]
            self.bdata[i][0] = y-1
            self.bdata[i][1] = x*-1
    def ckBlock(self,sx,sy):
        for i in self.bdata:
            x = (sx + i[0])
            y = (sy + i[1])
            if x > 9 or x < 0 or y > 19 or y < 0 or (x,y) in self.board.locked_pos:
                #print("sorry", x,y)
                return False
        return True
    def paint(self):
        self.board.fill()
    def chkmove(self,d):
        sc = 0
        if d == "u":
            self.rotate()
            if not self.ckBlock(self.x,self.y):
                self.rotate()
                self.rotate()
                self.rotate()
                self.addBlock(self.x,self.y)
            self.addBlock(self.x,self.y)
        if d == "r":
            if self.ckBlock(self.x+1,self.y):
                self.x +=1
                self.addBlock(self.x,self.y)
        if d == "l":
            if self.ckBlock(self.x-1,self.y):
                self.x-=1
                self.addBlock(self.x,self.y)
        if d == "d":
            if self.ckBlock(self.x,self.y+1):
                self.y+=1
                self.addBlock(self.x,self.y)
            else:
                for i in self.tetris.sprites():
                    self.addToGrid(i.x//settings.blockSize,i.y//settings.blockSize)
                self.paint()
                sc = self.board.line()
                sc += self.board.line()
                sc += self.board.line()
                self.spawn()
        self.paint()
        return sc
class Block(pygame.sprite.Sprite):
    def __init__(self,x,y,c) -> None:
        super().__init__()
        self.x = x
        self.y = y
        self.image = pygame.image.load(c)##pygame.Surface([settings.tilesize,settings.tilesize])
        # self.image.fill(settings.bbgc)
        self.rect = self.image.get_rect()
        self.update()
    def update(self):
        self.rect.topleft = (self.x,self.y)

pygame.init()
pygame.font.init()
nwg = Game()
clock = pygame.time.Clock()
nwg.spawnBlock()
down = pygame.USEREVENT
pygame.time.set_timer(down,300)
runs = 0
tim = 300
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            # os.system("cls")
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pass
            if event.key == pygame.K_UP:
                nwg.chk("u")
            if event.key == pygame.K_LEFT:
                nwg.chk("l")
            if event.key == pygame.K_RIGHT:
                nwg.chk("r")
            if event.key == pygame.K_DOWN:
                pygame.time.set_timer(down,30)
                if runs == 25:
                    runs = 0
            if event.key == pygame.K_CAPSLOCK:
                nwg.board.show()
                #print("\n")
            if event.key == pygame.K_LCTRL:
                pygame.time.wait(2000)
        if event.type == pygame.USEREVENT:
            if not nwg.update():
                bye(nwg.score)
            nwg.update()
            nwg.chk("d")
    if runs == 0:
        pygame.time.set_timer(down,300)
    runs+=1
    if runs == 25:
        runs = 0
    #pygame.draw.rect(nwg.screen,settings.bbgc,(settings.blockSize,settings.blockSize,settings.blockSize,settings.blockSize),0,3)
    drawGrid(nwg.screen)
    pygame.display.flip()
    clock.tick(settings.fps)