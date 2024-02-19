import random

def generateMap(width, groundMid, contrast):
    heightList = []
    ht = groundMid
    for i in range(width):
        ht += random.randint(-contrast, contrast)
        heightList.append(ht)
    return heightList

def smooth(heightMap):
    smoothedMap = heightMap.copy()
    for i in range(1, len(heightMap) - 1):
        smoothedMap[i] = (heightMap[i-1] + heightMap[i] + heightMap[i+1]) // 3
    return smoothedMap

def mapper2D(width, groundMid, contrast, smoothingLevels):
    heightMap = generateMap(width, groundMid, contrast)
    for i in range(smoothingLevels):
        heightMap = smooth(heightMap)
    return heightMap


import pygame


window_width, window_height = 1920, 1080
screen = pygame.display.set_mode((window_width, window_height))
tileSize = 16
tiles = []

class Map:
    @staticmethod
    def generateMap(ww=window_width, wh=window_height, ts=tileSize):
        heightMap = mapper2D(ww // ts,(wh // ts)//2,3,13)
        nb = wh // ts
        for x in range(0, ww // ts):
            tiles.append([])
            for y in range(0, wh // ts):
                if y > nb - heightMap[x]:
                    blocktype = (0, 200, 0)
                else:
                    blocktype = (102, 255, 255)
                tiles[x].append([x * ts, y * ts, blocktype])  # structure : xCord, yCord, blockType

    @staticmethod
    def render(tiles):
        for x in range(0, window_width // tileSize):
            for y in range(0, window_height // tileSize):
                pygame.draw.rect(screen, tiles[x][y][2], pygame.Rect(tiles[x][y][0], tiles[x][y][1], tileSize, tileSize))

Map.generateMap()

running = True
while running:
    screen.fill((0, 0, 0)) 
    Map.render(tiles)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
