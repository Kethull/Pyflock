import pygame
from pygame.math import Vector2
from pygame import draw
from boid import Boid
from spatialGrid import SpatialGrid
import random

boidList = []
obstacleList = []
grid = SpatialGrid(100)
mouseFollowStrength = 250
seperationRadius = 65
seperationStrength = 400
alignmentRadius = 20
alignmentStrength = 200
obstacleSize = 250
obstacleAvoidStrength = 3000

for i in range(1000):
    boidList.append(Boid(Vector2(random.randint(0, 1800), random.randint(0, 900)), Vector2(0, 0), Vector2(0, 0), 200, 200))
grid.addBoids(boidList)

obstacleList.append(Vector2(random.randint(0, 1800), random.randint(0, 900)))

pygame.init()
screen = pygame.display.set_mode((1800, 900))
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    deltaTime = clock.tick(60) / 1000.0

    for boid in boidList:
        boid.update(deltaTime)

    grid.empty()
    grid.addBoids(boidList)

    screen.fill((0, 0, 0))

    for boid in boidList:
        boid.drawBoid(screen)

    for obstacle in obstacleList:
        draw.circle(screen, (255, 255, 255), obstacle, obstacleSize)

    #Calculate forces on boids
    for boid in boidList:
        #Seperation
        seperationForce = Vector2(0, 0)
        seperationCount = 0
        for otherBoid in grid.query(boid.position.x, boid.position.y, seperationRadius):
            if otherBoid != boid:
                distance = boid.position.distance_to(otherBoid.position)
                if distance < seperationRadius:
                    seperationForce += (boid.position - otherBoid.position).normalize() / distance
                    seperationCount += 1

        if seperationCount > 0:
            seperationForce /= seperationCount
            seperationForce = seperationForce.normalize() * seperationStrength

        boid.addForce(seperationForce)

        #Alignment
        alignmentForce = Vector2(0, 0)
        alignmentCount = 0
        for otherBoid in grid.query(boid.position.x, boid.position.y, alignmentRadius):
            if otherBoid != boid:
                distance = boid.position.distance_to(otherBoid.position)
                if distance < alignmentRadius:
                    alignmentForce += otherBoid.velocity
                    alignmentCount += 1

        if alignmentCount > 0:
            alignmentForce /= alignmentCount
            alignmentForce = alignmentForce.normalize() * alignmentStrength

        boid.addForce(alignmentForce)

        #Mouse follow
        mouseFollowForce = Vector2(pygame.mouse.get_pos()) - boid.position
        mouseFollowForce = mouseFollowForce.normalize() * mouseFollowStrength

        boid.addForce(mouseFollowForce)

        #Obstacle avoidance
        obstacleAvoidForce = Vector2(0, 0)
        obstacleAvoidCount = 0
        for obstacle in obstacleList:
            distance = boid.position.distance_to(obstacle)
            if distance < obstacleSize:
                obstacleAvoidForce += (boid.position - obstacle).normalize() / distance
                obstacleAvoidCount += 1

        if obstacleAvoidCount > 0:
            obstacleAvoidForce /= obstacleAvoidCount
            obstacleAvoidForce = obstacleAvoidForce.normalize() * obstacleAvoidStrength

        boid.addForce(obstacleAvoidForce)
        
    #Update + draw every bird
    for boid in boidList:
        boid.update(deltaTime)
        boid.drawBoid(screen)

    draw.circle(screen, (255, 0, 0), pygame.mouse.get_pos(), 10)

    draw.circle(screen, (255, 255, 255), (0, 0), 50)
    draw.circle(screen, (255, 255, 255), (0, 0), 100)
    draw.circle(screen, (255, 255, 255), (0, 0), 150)
    draw.circle(screen, (255, 255, 255), (0, 0), 200)

    pygame.display.flip()
    
