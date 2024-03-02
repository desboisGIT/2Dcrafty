import pygame
import random


######## VARIABLES ########

WINDOW_WIDTH, WINDOW_HEIGHT = 1080, 720

BLOCKS=[
    (102,255,255),  #AIR
    (60,60,60),     #STONE
    (0,200,0),      #GRASS
    (80,40,0),      #DIRT
]

TILESIZE = 20
tileMap = []

gravity = 0.1
friction =0.9
jmpForce = 3
enmJmpForce = 4
speed = 3

Xvel,Yvel,grav = 0,0,0

######## /VARIABLES\ ########

######## INIT ########

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock() 
pygame.init()


# FPS Counter variables

fps_font = pygame.font.SysFont(None, 24)
fps_counter = 0
fps_update_frequency = 20

######## /INIT\ ########


######## CLASS & FUNCTIONS ######## 

class map():
    def generateMap(ww = WINDOW_WIDTH, wh = WINDOW_HEIGHT, ts = TILESIZE):
        a=8
        nb = wh//ts
        for i in range(0,wh//ts):
            tileMap.append([])
            for j in range(0,ww//ts):
                if i>nb-a:
                    tileMap[i].append([j*ts,i*ts,BLOCKS[3]])
                else:
                    tileMap[i].append([j*ts,i*ts,BLOCKS[0]])
    
    def initMap():
        screen.fill((0, 0, 0))
        for x in range(len(tileMap)):
            for y in range(len(tileMap[0])):
                pygame.draw.rect(screen, tileMap[x][y][2], pygame.Rect(tileMap[x][y][0], tileMap[x][y][1], TILESIZE, TILESIZE))
                         
    def updateMap(x,y): 
        try:
            pygame.draw.rect(screen, random.randint(0,255), pygame.Rect(tileMap[x][y][0], tileMap[x][y][1], TILESIZE, TILESIZE))
        except:
            pass
def fpsCounter():
    fps = clock.get_fps()
    fps_text = fps_font.render(f'FPS: {fps:.2f}', True, (255, 255, 255))
    pygame.draw.rect(screen, (0,0,0), pygame.Rect(0, 0, TILESIZE*6, TILESIZE*2))
    screen.blit(fps_text, (10, 10))

class Player:
    def __init__(self, x, y, Xvel=0, Yvel=0):
        self.posx = x
        self.posy = y
        self.Xvel = Xvel
        self.Yvel = Yvel
        self.width = TILESIZE
        self.height = TILESIZE*2
        self.on_ground = False 


    def move(self, dx, dy):

        self.posx += dx
        self.posy += dy


        for i in range(len(tileMap)):
            for j in range(len(tileMap[0])):
                if tileMap[i][j][2] != BLOCKS[0]:
                    block_rect = pygame.Rect(tileMap[i][j][0], tileMap[i][j][1], TILESIZE, TILESIZE)
                    player_rect = pygame.Rect(self.posx, self.posy, self.width, self.height)
                    if block_rect.colliderect(player_rect):
                        if dx > 0:
                            self.posx = tileMap[i][j][0] - self.width
                        elif dx < 0:
                            self.posx = tileMap[i][j][0] + TILESIZE
                        if dy > 0:
                            self.posy = tileMap[i][j][1] - self.height
                            self.on_ground = True
                            
                        elif dy < 0:
                            self.posy = tileMap[i][j][1] + TILESIZE
    def update(self):
        if self.Yvel < 15:
            self.Yvel += gravity 
        if self.on_ground:
            Yvel = 1
        self.move(0, self.Yvel)
        self.move(self.Xvel, 0)
        for i in range(-3, 3):
            for j in range(-3, 5):
                map.updateMap((self.posy // TILESIZE) + i, (self.posx // TILESIZE) + j)
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(self.posx, self.posy, TILESIZE, TILESIZE * 2))

                       
######## /CLASS & FUNCTIONS\ ######## 

map.generateMap()
map.initMap()

player1 = Player(100,100)
running = True

while(running):
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        
    if keys[pygame.K_LEFT] and player1.Xvel > -speed:
        player1.Xvel += -1
    if keys[pygame.K_RIGHT] and player1.Xvel < speed:
        player1.Xvel += 1
    if keys[pygame.K_UP] and player1.on_ground:
        player1.Yvel = -jmpForce
        player1.on_ground = False
    if keys[pygame.K_DOWN] and player1.Yvel < speed:
        player1.Yvel += 1
    

    player1.update()


    # FPS Counter
    fps_counter += 1
    if fps_counter == fps_update_frequency:
        fpsCounter()
        fps_counter = 0
    if fps_counter == 10:
        player1.Xvel = round(Xvel*friction,2)
        if 0-abs(Xvel)<0.2:
            player1.Xvel=0



    pygame.display.flip()
    clock.tick(200)

#   a faire:
#   
#  le system de rafraichisment local
#