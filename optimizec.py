import pygame
import math
import mapper2D
import random

######## DEBUG_MODE ################
debug_mode = True   # USE RESSOURCES
######## DEBUG_MODE ################


######## VARIABLES ########

TYPE_TILE = 2

TYPE_RIEN = 0
TYPE_TERRE = 1
TYPE_GRASS = 2
TYPE_DIRT = 3

WINDOW_WIDTH, WINDOW_HEIGHT = 1200, 1000


cam_pos = [0,0]

BLOCKS=[
    (102,255,255),  #AIR
    (60,60,60),     #STONE
    (0,200,0),      #GRASS
    (80,40,0),      #DIRT
    (107, 55, 17),  #WOOD
    (70,255,70),     #leafs
    (0, 153, 0)     #oaks leafs
]

TILESIZE = 20
tileMap = []

gravity = 0.1
friction =0.9
jmpForce = 5
enmJmpForce = 4
speed = 3
sizeMap =10
Count = 0.0

Xvel,Yvel,grav = 0,0,0

######## /VARIABLES\ ########

######## INIT ########
background = pygame.Surface((WINDOW_WIDTH*sizeMap, WINDOW_HEIGHT*sizeMap))
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
    @staticmethod
    def generateMap(ww = WINDOW_WIDTH, wh = WINDOW_HEIGHT, ts = TILESIZE):
        a=8
        heightMap = mapper2D.makeHeightMap(WINDOW_WIDTH*sizeMap,1,3,8,18,18)      
        nb = wh//ts
        for i in range(0,sizeMap*wh//ts):
            tileMap.append([])
            for j in range(0,sizeMap*ww//ts):
                height_index = j % len(heightMap) 
                height = heightMap[height_index]
                if i >= nb - height:
                    if tileMap[i-1][j][2] == BLOCKS[0]:
                        tileMap[i].append([j*ts,i*ts,BLOCKS[2]])
                    else:
                        tileMap[i].append([j*ts,i*ts,BLOCKS[3]])

                else:
                    tileMap[i].append([j*ts,i*ts,BLOCKS[0]])
            a+=1
    @staticmethod
    def initMap():
        screen.fill((0, 0, 0))
        for x in range(len(tileMap)):
            for y in range(len(tileMap[0])):
                pygame.draw.rect(background, tileMap[x][y][2], pygame.Rect(tileMap[x][y][0], tileMap[x][y][1], TILESIZE, TILESIZE))
    @staticmethod               
    def updateMap(x,y): 
        pygame.draw.rect(background, tileMap[x][y][2], pygame.Rect(tileMap[x][y][0], tileMap[x][y][1], TILESIZE, TILESIZE))
    
    def generateNature(frequency):
        index = 0

        while index < len(tileMap[0]) - frequency - 1:
            index += random.randint(3, frequency)
            y = 0
            while tileMap[y + 1][index][TYPE_TILE] == BLOCKS[0]:
                y += 1
            for i in range(random.randint(5, 8)):
                tileMap[y - i][index][TYPE_TILE] = BLOCKS[4]  # Wood blocks
                a=i
            
            treePatern = random.randint(0,2)
            if treePatern == 0:
                tileMap[y-a-1][index][TYPE_TILE] = BLOCKS[5]
                tileMap[y-a-2][index][TYPE_TILE] = BLOCKS[5]
                tileMap[y-a-1][index-1][TYPE_TILE] = BLOCKS[5]
                tileMap[y-a-2][index-1][TYPE_TILE] = BLOCKS[5]
                tileMap[y-a-2][index-2][TYPE_TILE] = BLOCKS[5]
                tileMap[y-a-1][index+1][TYPE_TILE] = BLOCKS[5]
                tileMap[y-a-2][index+1][TYPE_TILE] = BLOCKS[5]
                tileMap[y-a-2][index+2][TYPE_TILE] = BLOCKS[5]

                tileMap[y-a-4][index][TYPE_TILE] = BLOCKS[5]
                tileMap[y-a-3][index][TYPE_TILE] = BLOCKS[5]
                tileMap[y-a-4][index-1][TYPE_TILE] = BLOCKS[5]
                tileMap[y-a-3][index-1][TYPE_TILE] = BLOCKS[5]
                tileMap[y-a-4][index+1][TYPE_TILE] = BLOCKS[5]
                tileMap[y-a-3][index-2][TYPE_TILE] = BLOCKS[5]
                tileMap[y-a-3][index+2][TYPE_TILE] = BLOCKS[5]
                tileMap[y-a-3][index+1][TYPE_TILE] = BLOCKS[5]
            elif treePatern == 1:
                tileMap[y - a - 1][index][TYPE_TILE] = BLOCKS[6]
                tileMap[y - a - 1][index - 1][TYPE_TILE] = BLOCKS[6]
                tileMap[y - a - 1][index + 1][TYPE_TILE] = BLOCKS[6]
                tileMap[y - a - 2][index][TYPE_TILE] = BLOCKS[6]
                tileMap[y - a - 2][index - 1][TYPE_TILE] = BLOCKS[6]
                tileMap[y - a - 2][index + 1][TYPE_TILE] = BLOCKS[6]
                tileMap[y - a - 3][index][TYPE_TILE] = BLOCKS[6]
                tileMap[y - a - 3][index - 1][TYPE_TILE] = BLOCKS[6]
                tileMap[y - a - 3][index + 1][TYPE_TILE] = BLOCKS[6]
                tileMap[y - a - 4][index][TYPE_TILE] = BLOCKS[6]
                tileMap[y - a - 4][index - 1][TYPE_TILE] = BLOCKS[6]
                tileMap[y - a - 4][index + 1][TYPE_TILE] = BLOCKS[6]
                tileMap[y - a - 5][index][TYPE_TILE] = BLOCKS[6]
                tileMap[y - a - 5][index - 1][TYPE_TILE] = BLOCKS[6]
                tileMap[y - a - 5][index + 1][TYPE_TILE] = BLOCKS[6]
            elif treePatern == 2:
                for j in range(3):
                    tileMap[y - a - j - 1][index][TYPE_TILE] = (70, 255, 70)  # Pine color
                    tileMap[y - a - j - 1][index - 1][TYPE_TILE] = (70, 255, 70)  # Pine color
                    tileMap[y - a - j - 1][index + 1][TYPE_TILE] = (70, 255, 70)  # Pine color
                    tileMap[y - a - j - 2][index][TYPE_TILE] = (70, 255, 70)  # Pine color
                tileMap[y - a - 4][index][TYPE_TILE] = (70, 255, 70)  # Pine color



def fpsCounter():
    fps = clock.get_fps()
    fps_text = fps_font.render(f'FPS: {fps:.2f}', True, (255, 255, 255))
    pygame.draw.rect(fpsSurface, (0,0,0), pygame.Rect(0, 0, TILESIZE*6, TILESIZE*2))
    fpsSurface.blit(fps_text, (10, 10))

def isObstacle(x,y):
    try:
        isObstacle = False
        if tileMap[int(y//TILESIZE)][int(x//TILESIZE)][2] != BLOCKS[0]:
            isObstacle = True
        return isObstacle
    except:
        return True

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
        self.collidePointsList=[]


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

        self.collidePointsList=[
            [x+1,y+1],                                    # TOP LEFT
            [x-1+TILESIZE,y+1],                           # TOP RIGHT
            [x-1+TILESIZE,y+TILESIZE-1],                  # MIDDLE RIGHT
            [x+1,y+TILESIZE-1],                           # MIDDLE LEFT
            [x+1,y+TILESIZE*2-1],                         # BUTTOM LEFT
            [x-1+TILESIZE,y+TILESIZE*2-1],                # BUTTOM RIGHT 
        ]
        for points in self.collidePointsList:
            pygame.draw.circle(screen, (255,0,0), (points), 1)
            if isObstacle(points[0],points[1]):
                return True
        return False

    def update(self):
        if self.Yvel < 15:
            self.Yvel += 3.0*gravity 

        self.move(0, self.Yvel)
        self.move(self.Xvel, 0)
        pygame.draw.rect(entitySurface, (255, 0, 0), pygame.Rect(self.posx, self.posy, TILESIZE, TILESIZE * 2))



                       
######## /CLASS & FUNCTIONS\ ######## 



player1 = Player(1000,500)
running = True
loadingScreen = True
menuscreen = True


start_button_rect = pygame.Rect(WINDOW_WIDTH//2-100, WINDOW_HEIGHT//2-50, 200, 100)
start_button_color = (0, 255, 0)

while menuscreen:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:

                if start_button_rect.collidepoint(event.pos):
                    menuscreen = False
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, start_button_color, start_button_rect)
    start_font = pygame.font.SysFont(None, 36)
    start_text = start_font.render("Start", True, (0, 0, 0))
    text_rect = start_text.get_rect(center=start_button_rect.center)
    screen.blit(start_text, text_rect)
    pygame.display.flip()

while loadingScreen:
    loading_text = fps_font.render("Generating map...", True, (255, 255, 255))
    screen.fill((0, 0, 0))
    screen.blit(loading_text, (WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2))
    pygame.display.flip()
    map.generateMap()
    loading_text = fps_font.render("Generating nature...", True, (255, 255, 255))
    map.generateNature(17)
    screen.fill((0, 0, 0))
    screen.blit(loading_text, (WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2))
    pygame.display.flip()
    loadingScreen = False
  

map.initMap()

while(running):
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            mouseClick = list(pos)
            print(pos,mouseClick)
            mouseClick[0] += cam_pos[0]
            mouseClick[1] += cam_pos[1]
            if event.button == 1:
                isObstacle(mouseClick[0],mouseClick[1])
                tileMap[round(mouseClick[1]//TILESIZE)][mouseClick[0]//TILESIZE][2] = BLOCKS[3]
                map.updateMap(round(mouseClick[1]//TILESIZE),mouseClick[0]//TILESIZE)
                if debug_mode:
                    print(isObstacle(mouseClick[0],mouseClick[1]), "   ", mouseClick[0],"   ", mouseClick[1])
            if event.button == 3:
                isObstacle(mouseClick[0],mouseClick[1])
                tileMap[round(mouseClick[1]//TILESIZE)][mouseClick[0]//TILESIZE][2] = BLOCKS[0]
                map.updateMap(round(mouseClick[1]//TILESIZE),mouseClick[0]//TILESIZE)
                if debug_mode:
                    print(isObstacle(mouseClick[0],mouseClick[1]), "   ", mouseClick[0],"   ", mouseClick[1])
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_k:
                debug_mode = not debug_mode
                print("debug mode: ",debug_mode)

    if keys[pygame.K_LEFT] and player1.Xvel > -speed:
        player1.Xvel += -1
    if keys[pygame.K_RIGHT] and player1.Xvel < speed:
        player1.Xvel += 1
    if keys[pygame.K_UP] and player1.on_ground:
        player1.Yvel = -jmpForce
        player1.on_ground = False
        player1.colle_au_sol = False
    if keys[pygame.K_DOWN] and player1.Yvel < speed:
        player1.Yvel += 1
    

    

    player1.update()

    frameCount += 1

    Count += 1.0

    if debug_mode:     # FPS Counter
        fps_counter += 1
        if fps_counter == fps_update_frequency:
            fpsCounter()
            fps_counter = 0

    if frameCount == 10:
        player1.Xvel = round(Xvel*friction,2)
        if 0-abs(Xvel)<0.2:
            player1.Xvel=0
        
        frameCount=0

    
    #cam_pos = [player1.posx-WINDOW_WIDTH//2,player1.posy-WINDOW_HEIGHT//1.5]
    cam_pos[0] = max(0, min(player1.posx - WINDOW_WIDTH // 2, sizeMap * WINDOW_WIDTH - WINDOW_WIDTH))
    cam_pos[1] = max(0, min(player1.posy - WINDOW_HEIGHT // 1.5, sizeMap * WINDOW_HEIGHT - WINDOW_HEIGHT))

    screen.blit(background,(0,0),(cam_pos[0],cam_pos[1],2*WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.blit(entitySurface,(player1.posx-cam_pos[0],player1.posy-cam_pos[1]))
    if debug_mode: 
        for points in player1.collidePointsList:
            pygame.draw.circle(screen, (255,0,0), (points[0]-cam_pos[0],points[1]-cam_pos[1]), 1)
    screen.blit(fpsSurface,(0,0))
    pygame.display.flip()
    clock.tick(999)

