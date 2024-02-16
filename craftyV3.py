import pygame
import random

WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
TILE_SIZE = 30

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
running = True


speed = 4
renderListX = []


blockType = [
    (50, 100, 255),  # [0] Air (White)
    (0, 255, 0),      # [1] Grass (Green)
    (139, 69, 19),    # [2] Dirt (Brown)
    (128, 128, 128),  # [3] Stone (Gray)
    (139, 69, 19),    # [4] Wood (Brown)
    (0, 128, 0)       # [5] Leaves (Dark Green)
]

def mapGen(width, height, tileSize): #in blocks
    tileMap = []
    h = 50
    
    for y in range(0,int(height),tileSize):
        tileMap.append([])
        for x in range(0,int(width),tileSize):
            if (y//tileSize) > h:
                purpif = random.randint(0,1)
                if purpif ==1:
                    tileMap[y//tileSize].append([x,y,blockType[2]])
                else: 
                    tileMap[y//tileSize].append([x,y,blockType[3]])
            else:
                tileMap[y//tileSize].append([x,y,blockType[0]])

    return tileMap

tileMap=mapGen(WINDOW_WIDTH*1.5, WINDOW_HEIGHT*2, TILE_SIZE) #  tile[0] = x,  tile[1] = y,  tile[2] = color
"""
def render(tiles, tileSize):
    for y in range(len(tiles)):
        for x in range(len(tiles[y])):
            pygame.draw.rect(screen, tiles[y][x][2], pygame.Rect(tiles[y][x][0], tiles[y][x][1], tileSize, tileSize))
    pygame.draw.rect(screen, (0,255,0), pygame.Rect(player1.posx, player1.posy, tileSize, tileSize*2))
"""
class Player:
    def __init__(self, x, y):
        self.posx = x
        self.posy = y
        self.width = TILE_SIZE
        self.height = TILE_SIZE*2
        self.on_ground = False

    def move(self, dx, dy):
        self.posx += dx
        self.posy += dy
        
        for i in range(len(tileMap)):
            for j in range(len(tileMap[0])):
                if tileMap[i][j][2] != blockType[0]:
                    block_rect = pygame.Rect(tileMap[i][j][0], tileMap[i][j][1], TILE_SIZE, TILE_SIZE)
                    player_rect = pygame.Rect(self.posx, self.posy, self.width, self.height)
                    if block_rect.colliderect(player_rect):
                        if dx > 0:
                            self.posx = tileMap[i][j][0] - self.width
                        elif dx < 0:
                            self.posx = tileMap[i][j][0] + TILE_SIZE
                        if dy > 0:
                            self.posy = tileMap[i][j][1] - self.height
                            self.on_ground = True
                        elif dy < 0:
                            self.posy = tileMap[i][j][1] + TILE_SIZE
class Camera():
    def __init__(self, width, height, tile_map):
        self.width = width
        self.height = height
        self.tile_map = tile_map
        self.x = 0
        self.y = 0

    def apply(self, entity):
        return entity[0] - self.x, entity[1] - self.y

    def update(self, target):
        self.x = target.posx - (self.width // 2)
        self.y = target.posy - (self.height // 2)

        # Keep camera in bounds of the map
        self.x = max(0, min(self.x, len(self.tile_map[0]) * TILE_SIZE - self.width))
        self.y = max(0, min(self.y, len(self.tile_map) * TILE_SIZE - self.height))

player1 = Player(1920,1080)
camera = Camera(player1.posx,player1.posy, tileMap)

while running:
    ev = pygame.event.get()
    keys = pygame.key.get_pressed()

    if keys[pygame.K_ESCAPE]:
        running = False
    if keys[pygame.K_LEFT]:
        player1.move(-speed,0)
    if keys[pygame.K_RIGHT]:
        player1.move(speed,0)
    if keys[pygame.K_UP]:
        player1.move(0,-speed)
    if keys[pygame.K_DOWN]:
        player1.move(0,speed)

    camera.update(player1)

    screen.fill((0, 0, 0))  # Clear the screen

    for y in range(len(tileMap)):
        for x in range(len(tileMap[0])):
            tile_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if tile_rect.colliderect(pygame.Rect(camera.x, camera.y, camera.width, camera.height)):
                pygame.draw.rect(screen, tileMap[y][x][2], tile_rect.move(-camera.x, -camera.y))

    pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(player1.posx - camera.x, player1.posy - camera.y, TILE_SIZE, TILE_SIZE * 2))
    pygame.display.flip()
