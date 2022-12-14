# fix errors
import math
import numpy as np
from pygame.math import Vector2
from pygame import draw


class Boid:
    # TODO: go through all setMag methods and change to magnitude.set
    # TODO: pass in all global vars as parameters

    def __init__(self, _position):
        self.position = _position
        self.velocity = Vector2(0, 0)
        self.acceleration = Vector2(0, 0)
        self.separationForce = Vector2(0, 0)
        self.alignmentForce = Vector2(0, 0)
        self.isBirdZero = False

    def update(self, deltaTime):
        # todo: refactor into functions
        # Acceleration changes velocity
        self.velocity.add(self.acceleration * deltaTime)

        # Limit velocity
        if self.velocity.magnitude_squared > maxSpeed * maxspeed:
            self.velocity.magnitude = maxSpeed

        # Velocity changes position
        self.position += self.velocity * deltaTime

        # wrap boids around screen
        if self.position.x > self.screenWidth:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = self.screenWidth

        if self.position.y > self.screenHeight:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = self.screenHeight

    def calculateAcceleration(self, grid):
        self.acceleration = Vector2(0, 0)

        # avoid obstacles
        for obstacle in self.obstacles:
            vectorToObstacle = obstacle.position - self.position
            squareDistanceToObstacle = vectorToObstacle.magnitude_squared()
            if squareDistanceToObstacle < obstacleSize * obstacleSize:
                distanceToObstacle = math.sqrt(squareDistanceToObstacle)
                obstacleAvoidAmount = 1 - (distanceToObstacle / obstacleSize)
                self.acceleration.add(vectorToObstacle.normalize() * obstacleAvoidAmount * 100)

        # TODO: refactor each of the below functions to use the grid

        alignment = self.align(grid)
        cohesion = self.cohere(grid)
        separation = self.separate(grid)
        avoidance = self.avoid()

        self.acceleration += alignment
        self.acceleration += cohesion
        self.acceleration += separation
        self.acceleration += avoidance

    def align(self, grid):
        self.alignmentForce = Vector2(0, 0)

        averageVelocityOfNeighbours = Vector2(0, 0)
        alignmentNeighbourCount = 0

        for otherBird in grid.query(self.position.x, self.position.y, BIRD_ALIGNMENT_RADIUS):
            if otherBird == self:
                continue

            vectorToOtherBird = otherBird.position - self.position
            squareDistanceToOtherBird = vectorToOtherBird.magnitude_squared()

            # Ignore if too far away
            if squareDistanceToOtherBird > BIRD_ALIGNMENT_RADIUS*BIRD_ALIGNMENT_RADIUS:
                continue

            # Accumulate average heading
            alignmentNeighbourCount += 1
            averageVelocityOfNeighbours.add(otherBird.velocity)

        if alignmentNeighbourCount > 0:
            averageVelocityOfNeighbours.mult(1.0 / alignmentNeighbourCount)
            self.alignmentForce.magnitude.set(averageVelocityOfNeighbours.magnitude.set(BIRD_ALIGNMENT_STRENGTH))
            self.acceleration.add(self.alignmentForce)

    def cohere(self, boids):
        steering = Vector2(0, 0)
        total = 0
        for boid in boids:
            if boid != self:
                distance = self.position.distance_to(boid.position)
                if distance > 0 and distance < 100:
                    steering += boid.position
                    total += 1
        if total > 0:
            steering /= total
            steering -= self.position
            steering = steering.normalize() * maxSpeed
            steering -= self.velocity
            steering = steering.limit(self.maxForce)
        return steering

    def separate(self, boids):
        steering = Vector2(0, 0)
        total = 0
        for boid in boids:
            if boid != self:
                distance = self.position.distance_to(boid.position)
                if distance > 0 and distance < 25:
                    diff = self.position - boid.position
                    diff = diff.normalize() / distance
                    steering += diff
                    total += 1
        if total > 0:
            steering /= total
            steering = steering.normalize() * maxSpeed
            steering -= self.velocity
            steering = steering.limit(self.maxForce)
        return steering

    def avoid(self):
        steering = Vector2(0, 0)
        total = 0
        for boid in boids:
            distance = self.position.distance_to(boid.position)
            if distance > 0 and distance < 100:
                diff = self.position - boid.position
                diff = diff.normalize() / distance
                steering += diff
                total += 1
        if total > 0:
            steering /= total
            steering = steering.normalize() * maxSpeed
            steering -= self.velocity
            steering = steering.limit(self.maxForce)
        return steering

    def drawBoid(self, screen):
        draw.circle(screen, (255, 255, 255),
                    (int(self.position.x), int(self.position.y)), 5)
