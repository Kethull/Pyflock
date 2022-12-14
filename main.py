import pygame
from pygame.math import Vector2
from pygame import draw
from boid import Boid
from spatialGrid import SpatialGrid
import random

boidList = []
obstacleList = []
grid = SpatialGrid(100)
previousMiliseconds = 0

pygame.init()
screen = pygame.display.set_mode((1800, 900))
clock = pygame.time.Clock()

for i in range(1000):
    randomPosition = Vector2(random.randint(0, screen.get_width/2), random.randint(0, screen.get_height/2))
    boid = Boid(randomPosition)
    boid.update(random.random(0, 1))
    boidList.append(boid)

#obstacleList.append(Vector2(random.randint(0, 1800), random.randint(0, 900)))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    mouseFollowStrength = 250
    seperationRadius = 65
    seperationStrength = 400
    alignmentRadius = 20
    alignmentStrength = 200
    obstacleSize = 250
    obstacleAvoidStrength = 3000
    maxSpeed = 200

    # calculate elapsed time in miliseconds
    currentMiliseconds = pygame.time.get_ticks()
    deltaTime = (currentMiliseconds - previousMiliseconds)
    previousMiliseconds = currentMiliseconds

    grid.empty()
    for boid in boidList:
        grid.add(boid.position.x, boid.position.y)

    for obstacle in obstacleList:
        draw.circle(screen, (255, 255, 255), obstacle, obstacleSize)

    for boid in boidList
    boid.calculateAcceleration(grid)

    -------------------------------------------------

    screen.fill((0, 0, 0))

    for boid in boidList:
        boid.drawBoid(screen)

    # Calculate forces on boids
    for boid in boidList:
        boid.calculateAcceleration(boidList)
        boid.update(deltaTime)
        boid.drawBoid(screen)

    if pygame.mouse.get_pressed()[0]:
        obstacleList.append(Vector2(pygame.mouse.get_pos()[
                            0], pygame.mouse.get_pos()[1]))

    pygame.display.flip()
