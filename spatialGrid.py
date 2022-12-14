import pygame
from pygame.math import Vector2
from pygame import draw


class SpatialGrid:
    def __init__(self, cellSize):
        self.cellSize = cellSize
        self.grid = []
        self.gridWidth = 0
        self.gridHeight = 0

    def empty(self):
        self.grid = []

    def add(self, x, y, boid):
        gridX = int(x // self.cellSize)
        gridY = int(y // self.cellSize)

        if gridX < 0 or gridY < 0 or gridX >= self.gridWidth or gridY >= self.gridHeight:
            return

        self.grid[gridX][gridY].append(boid)

    def getCell(self, x, y):
        gridX = int(x // self.cellSize)
        gridY = int(y // self.cellSize)

        if gridX < 0 or gridY < 0 or gridX >= self.gridWidth or gridY >= self.gridHeight:
            return []

        return self.grid[gridX][gridY]

    def query(self, x, y, radius):
        gridX = int(x // self.cellSize)
        gridY = int(y // self.cellSize)

        results = []
        for i in range(gridX - 1, gridX + 2):
            for j in range(gridY - 1, gridY + 2):
                if i < 0 or j < 0 or i >= self.gridWidth or j >= self.gridHeight:
                    continue

                cell = self.grid[i][j]
                for boid in cell:
                    distance = Vector2(x, y).distance_to(boid.position)
                    if distance < radius:
                        results.append(boid)

        return results

    def draw(self, screen):
        for i in range(0, self.gridWidth):
            for j in range(0, self.gridHeight):
                x = i * self.cellSize
                y = j * self.cellSize
                # change this to a white rectangle
                draw.rect(screen, (255, 255, 255),
                          (x, y, self.cellSize, self.cellSize), 1)

    def debugDraw(self, screen):
        for i in range(0, self.gridWidth):
            for j in range(0, self.gridHeight):
                x = i * self.cellSize
                y = j * self.cellSize
                draw.rect(screen, (0, 0, 0),
                          (x, y, self.cellSize, self.cellSize), 1)
