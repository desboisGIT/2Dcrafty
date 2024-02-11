import pygame 
import random



window_width, window_height = 1080, 720
screen = pygame.display.set_mode((window_width, window_height))
tileSize = 16 
tiles=[]
#up to dattte

LEFT = 1
RIGHT = 3


blocks=[
    ['air',(102,255,255)],
    ['stone',(60,60,60)],
    ['grass',(0,200,0)],
    ['dirt',(80,40,0)],
]
sellected_block = blocks[1]
blocktype='dirt'
gravity = 0.1
friction =0.7
jmpForce = 3
enmJmpForce = 4
speed = 15

Xvel,Yvel,grav = 0,0,0


class Player:
    def __init__(self, x, y):
        self.posx = x
        self.posy = y
        self.width = 16
        self.height = 32
        self.on_ground = False  # Reset on_ground flag
          # Flag to indicate if the player is on the ground

    def move(self, dx, dy):
        # Move the player
        self.posx += dx
        self.posy += dy
        
        # Check for collisions with non-air blocks

        for i in range(len(tiles)):
            for j in range(len(tiles[0])):
                if tiles[i][j][2][0] != 'air':
                    block_rect = pygame.Rect(tiles[i][j][0], tiles[i][j][1], tileSize, tileSize)
                    player_rect = pygame.Rect(self.posx, self.posy, self.width, self.height)
                    if block_rect.colliderect(player_rect):
                        # If collision detected, adjust player position to avoid collision
                        if dx > 0:
                            self.posx = tiles[i][j][0] - self.width
                        elif dx < 0:
                            self.posx = tiles[i][j][0] + tileSize
                        if dy > 0:
                            self.posy = tiles[i][j][1] - self.height
                            self.on_ground = True
                            
                        elif dy < 0:
                            self.posy = tiles[i][j][1] + tileSize
class map():
    def generateMap(ww = window_width, wh= window_height, ts=tileSize):
        a=8
        nb = wh//tileSize
        for i in range(0,wh//tileSize):
            tiles.append([])
            for j in range(0,ww//tileSize):
                if i>nb-a:
                        blocktype = ['grass',(0,200,0)]
                else:
                        blocktype = ['air',(102,255,255)]
                tiles[i].append([j*ts,i*ts,blocktype]) #structure : xCord, yCord, blockType
            
            
#    def drawMap():
#        for i in range(0, window_height // tileSize):
#            for j in range(0, window_width // tileSize):
                
    def updateMap():   
        screen.fill((0, 0, 0))
        for i in range(0, window_height // tileSize):
            for j in range(0, window_width // tileSize):
                if tiles[i-1][j][2][0] != 'air' and tiles[i][j][2][0] == "grass":
                    tiles[i][j][2] = ['dirt',(80,40,0)]
                pygame.draw.rect(screen, tiles[i][j][2][1], pygame.Rect(tiles[i][j][0], tiles[i][j][1], tileSize, tileSize))

class Mobs:
    def __init__(self, x, y, xVe, Yve):
        self.posx = x
        self.posy = y
        self.yVel = Yve
        self.width = 16
        self.height = 32
        self.on_ground = False  # Reset on_ground flag
          # Flag to indicate if the player is on the ground

    def move(self, dx, dy):

        self.posx += dx
        self.posy += dy
        if grav < 15:
            self.yVel += gravity
        if mob1.on_ground == True:
            self.yVel = 1
        # Check for collisions with non-air blocks

        for i in range(len(tiles)):
            for j in range(len(tiles[0])):
                if tiles[i][j][2][0] != 'air':
                    block_rect = pygame.Rect(tiles[i][j][0], tiles[i][j][1], tileSize, tileSize)
                    mob_rect = pygame.Rect(self.posx, self.posy, self.width, self.height)
                    if block_rect.colliderect(mob_rect):
                        # If collision detected, adjust player position to avoid collision
                        if dx > 0:
                            self.posx = tiles[i][j][0] - self.width
                        elif dx < 0:
                            self.posx = tiles[i][j][0] + tileSize
                        if dy > 0:
                            self.posy = tiles[i][j][1] - self.height
                            self.on_ground = True
                            
                        elif dy < 0:
                            self.posy = tiles[i][j][1] + tileSize
    def mobPathFind(self):

        posMob = [self.posx, self.posy]
        posPlayer = [player1.posx, player1.posy]
        iY,iX,indexY,indexX=0,0,0,0
        while iY < posMob[1]:
            iY+=tileSize
            indexY+=1
            while iX < posMob[0]:
                iX+=tileSize
                indexX+=1
        indexX -=1
        indexY -=1 
        if posMob[0] < posPlayer[0]:
            print("TO THE RIGHTTT")
            mob1.move(1, 0)
            if self.on_ground:
                if tiles[indexY+1][indexX+2][2][0] != 'air' or tiles[indexY+2][indexX+2][2][0] != 'air': # droite
                    self.yVel = -enmJmpForce
                    print("a droitttttetetete")
                    self.on_ground = False
        elif posMob[0] > posPlayer[0]:
            print("TO THE LEFFTTT")
            mob1.move(-1, 0)
            if self.on_ground:
                if tiles[indexY+1][indexX][2][0] != 'air' or tiles[indexY+2][indexX][2][0] != 'air': # droite
                    self.yVel = -enmJmpForce
                    print("a gaucheeeeeeeeeeeeee")
                    self.on_ground = False












"""
        if posMob[1] < posPlayer[1]:
            print("TO THE BOTTOM")
        elif posMob[1] > posPlayer[1]:
            print("TO THE TOPPP")
"""





mob1 = Mobs(200, 100,0,0)
player1 = Player(100, 100)
map.generateMap()
map.updateMap()

print(tiles)
running = True
while(running):
    ev = pygame.event.get()
    keys = pygame.key.get_pressed()
    for event in ev:
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if event.button == 1:

                iY,iX,indexY,indexX=0,0,0,0
                while iY < pos[1]:
                    iY+=tileSize
                    indexY+=1
                    while iX < pos[0]:
                        iX+=tileSize
                        indexX+=1
                try:
                    tiles[indexY-1][indexX-1][2] = ['air',(102,255,255)]
                except:
                    print("out of range???")
            elif event.button == 2:
                pass 

            elif event.button == 3:
                iY,iX,indexY,indexX=0,0,0,0
                while iY < pos[1]:
                    iY+=tileSize
                    indexY+=1
                    while iX < pos[0]:
                        iX+=tileSize
                        indexX+=1
                indexX -=1
                indexY -=1
                        
                try:

                    if tiles[indexY][indexX][2][0] == 'air':
                        if (tiles[indexY+1][indexX][2][0] != 'air' or 
                            tiles[indexY][indexX+1][2][0] != 'air' or 
                            tiles[indexY-1][indexX][2][0] != 'air' or 
                            tiles[indexY][indexX-1][2][0] != 'air'):
                                tiles[indexY][indexX][2] = sellected_block
                except:
                    print("out of range???")
            






    if keys[pygame.K_LEFT] and Xvel > -speed:
        Xvel += -1
    if keys[pygame.K_RIGHT] and Xvel < speed:
        Xvel += 1
    if keys[pygame.K_UP] and player1.on_ground:  # Only jump if on the ground
        Yvel = -jmpForce
        player1.on_ground = False
    if keys[pygame.K_DOWN] and Yvel < speed:
        Yvel += 1
   

    Xvel *= friction

    if Yvel < 15:
        Yvel += gravity  # Apply gravity when not on the ground
    if player1.on_ground == True:
        Yvel = 1

        #print(player1.on_ground)
    player1.move(0, Yvel)
    player1.move(Xvel, 0)
    mob1.move(0, mob1.yVel)
    mob1.mobPathFind()
    map.updateMap()
    pygame.draw.rect(screen, (255,0,0), pygame.Rect(player1.posx, player1.posy, tileSize, tileSize*2))
    pygame.draw.rect(screen, (50,100,150), pygame.Rect(mob1.posx, mob1.posy, tileSize, tileSize*2))
    pygame.display.flip()
