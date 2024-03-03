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
jmpForce = 5
enmJmpForce = 4
speed = 3

Xvel,Yvel,grav = 0,0,0

######## /VARIABLES\ ########

######## INIT ########
background = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
entitySurface = pygame.Surface((TILESIZE, TILESIZE*2))
fpsSurface = pygame.Surface((120, 60))
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock() 
pygame.init()


# FPS Counter variables

fps_font = pygame.font.SysFont(None, 24)
fps_counter = 0
fps_update_frequency = 100
frameCount = 0

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
                pygame.draw.rect(background, tileMap[x][y][2], pygame.Rect(tileMap[x][y][0], tileMap[x][y][1], TILESIZE, TILESIZE))
                         
    def updateMap(x,y): 
        try:
            pygame.draw.rect(background, random.randint(0,255), pygame.Rect(tileMap[x][y][0], tileMap[x][y][1], TILESIZE, TILESIZE))
        except:
            pass


def fpsCounter():
    fps = clock.get_fps()
    fps_text = fps_font.render(f'FPS: {fps:.2f}', True, (255, 255, 255))
    pygame.draw.rect(fpsSurface, (0,0,0), pygame.Rect(0, 0, TILESIZE*6, TILESIZE*2))
    fpsSurface.blit(fps_text, (10, 10))

def isObstacle(x,y):
    isObstacle = False
    if tileMap[int(y//TILESIZE)][int(x//TILESIZE)][2] != BLOCKS[0]:
        isObstacle = True

    #print("click : x,y = ",x,y,"   tiles[i,j] ",y//TILESIZE,x//TILESIZE,"   ", isObstacle)

    return isObstacle

class Player:
    def __init__(self, x, y, Xvel=0, Yvel=0):
        self.posx = x
        self.posy = y
        self.Xvel = Xvel
        self.Yvel = Yvel
        self.width = TILESIZE
        self.height = TILESIZE*2
        self.on_ground = False
        self.colle_au_sol = False


    def move(self, dx, dy):
        new_x = self.posx + dx
        new_y = self.posy + dy


        if not self.check_collision(new_x, new_y):
            self.posx = new_x
            self.posy = new_y
        else : ##### collision !!
            self.Yvel = 0
            self.on_ground = True
            if not self.colle_au_sol :
                self.posy -= (self.posy) % TILESIZE
                self.colle_au_sol = True

    def check_collision(self, x, y):

        collidePointsList=[
            [x+1,y+1],                                    # TOP LEFT
            [x-1+TILESIZE,y+1],                           # TOP RIGHT
            [x-1+TILESIZE,y+TILESIZE-1],                  # MIDDLE RIGHT
            [x+1,y+TILESIZE-1],                           # MIDDLE LEFT
            [x+1,y+TILESIZE*2-1],                         # BUTTOM LEFT
            [x-1+TILESIZE,y+TILESIZE*2-1],                # BUTTOM RIGHT 
        ]
        for points in collidePointsList:
            if isObstacle(points[0],points[1]):
                return True
        return False
    """
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
    """


    def update(self):

        #player1.on_ground = False

        if self.Yvel < 15:
            self.Yvel += 3.0*gravity 

        self.move(0, self.Yvel)
        self.move(self.Xvel, 0)
        pygame.draw.rect(entitySurface, (255, 0, 0), pygame.Rect(self.posx, self.posy, TILESIZE, TILESIZE * 2))

                       
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
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if event.button == 1:
                isObstacle(pos[0],pos[1])
                tileMap[pos[1]//TILESIZE][pos[0]//TILESIZE][2] = BLOCKS[3]
                map.updateMap(pos[1]//TILESIZE,pos[0]//TILESIZE)
                #print(isObstacle(pos[0],pos[1]), "   ", pos[0],"   ", pos[1])
    
    if keys[pygame.K_LEFT] and player1.Xvel > -speed:
        player1.Xvel += -1
    if keys[pygame.K_RIGHT] and player1.Xvel < speed:
        player1.Xvel += 1
    if keys[pygame.K_UP] and player1.on_ground:
        player1.Yvel = -jmpForce
        #player1.on_ground = False
        player1.colle_au_sol = False
    if keys[pygame.K_DOWN] and player1.Yvel < speed:
        player1.Yvel += 1
    

    player1.update()


    # FPS Counter
    fps_counter += 1
    frameCount += 1
    if fps_counter == fps_update_frequency:
        fpsCounter()
        fps_counter = 0

    if frameCount == 10:
        player1.Xvel = round(Xvel*friction,2)
        if 0-abs(Xvel)<0.2:
            player1.Xvel=0
        
        frameCount=0


    screen.blit(background,(0,0))
    screen.blit(entitySurface,(player1.posx,player1.posy))
    screen.blit(fpsSurface,(0,0))
    pygame.display.flip()
    clock.tick(500)

