# fix errors
import numpy as np
from pygame.math import Vector2
from pygame import draw


class Boid:
    # create Vector2 for position, velocity, acceleration

    def __init__(self, _position):
        self.position = _position
        self.velocity = Vector2(0, 0)
        self.acceleration = Vector2(0, 0)
        self.separationForce = Vector2(0, 0)
        self.alignmentForce = Vector2(0, 0)
        self.isBirdZero = False

    def update(self, deltaTime):
        self.velocity = self.velocity + self.acceleration * deltaTime
        if self.velocity.length() > self.maxSpeed:
            self.velocity = self.velocity.normalize() * self.maxSpeed
        self.position = self.position + self.velocity * deltaTime
        self.acceleration = Vector2(0, 0)

    def calculateAcceleration(self, boids):
        alignment = self.align(boids)
        cohesion = self.cohere(boids)
        separation = self.separate(boids)
        avoidance = self.avoid()

        alignment *= 1.0
        cohesion *= 1.0
        separation *= 1.5
        avoidance *= 10.0

        self.acceleration += alignment
        self.acceleration += cohesion
        self.acceleration += separation
        self.acceleration += avoidance

    def align(self, boids):
        steering = Vector2(0, 0)
        total = 0
        for boid in boids:
            if boid != self:
                distance = self.position.distance_to(boid.position)
                if distance > 0 and distance < 100:
                    steering += boid.velocity
                    total += 1
        if total > 0:
            steering /= total
            steering = steering.normalize() * self.maxSpeed
            steering -= self.velocity
            steering = steering.limit(self.maxForce)
        return steering

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
            steering = steering.normalize() * self.maxSpeed
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
            steering = steering.normalize() * self.maxSpeed
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
            steering = steering.normalize() * self.maxSpeed
            steering -= self.velocity
            steering = steering.limit(self.maxForce)
        return steering

    def drawBoid(self, screen):
        draw.circle(screen, (255, 255, 255),
                    (int(self.position.x), int(self.position.y)), 5)
