"""
Tidal Forces Simulation
Credit to adammoyle from StackExchange for orbital simulation code
"""

import pygame, math
from pygame.locals import *
from random import randint
pygame.init()
screen = pygame.display.set_mode([0, 0], pygame.FULLSCREEN)
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (128, 128, 128)
YELLOW = (255, 255, 0)

# The gravitational constant G
G = 6.67428e-11

class Planet():
    def __init__(self, vel = [1, 1], color = BLACK, name = None, diam = 10, mass = 100000, pos = [100, 100]):
        self.v = vel[:]
        self.m = mass
        self.mass = mass/1000000
        self.pos = pos[:]
        self.color = color
        self.r = diam / 2
        self.name = name

    def attraction(self, other):
        if self is other:
            raise ValueError("Attraction of object %r to itself requested"
                             % self.name)
        sx, sy = self.pos[0], self.pos[1]
        ox, oy = other.pos[0], other.pos[1]

        dx = (ox - sx)
        dy = (oy - sy)
        d = math.sqrt(dx ** 2 + dy ** 2)

        # Report an error if the distance is zero; otherwise we'll
        # get a ZeroDivisionError exception further down.
        if d == 0:
            raise ValueError("Collision between objects %r and %r"
                             % (self.name, other.name))

        # Compute the force of attraction
        f = G * self.mass * other.mass / (d ** 2)

        # Compute the direction of the force.
        theta = math.atan2(dy, dx)
        fx = math.cos(theta) * f
        fy = math.sin(theta) * f
        print(fx, fy)
        return fx, fy

    def update(self):
        # Update positions
        self.pos[0] += self.v[0]
        self.pos[1] += self.v[1]

class World():
    def __init__(self, planetList):
        self.plnt = planetList

    def draw(self):
        for p in self.plnt:
            pygame.draw.circle(screen, p.color, [math.ceil(p.pos[0]), math.ceil(p.pos[1])], math.ceil(p.r), 0)

    def update(self):
        timestep = 3600
        force = {}
        for p in self.plnt:
            total_fx = total_fy = 0.0
            for q in self.plnt:
                if p is q:
                    continue
                fx, fy = p.attraction(q)
                total_fx += fx
                total_fy += fy
            force[p] = (total_fx, total_fy)

        for body in self.plnt:
            fx, fy = force[body]
            body.v[0] += fx / body.mass * timestep
            body.v[1] += fy / body.mass * timestep

            body.update()

        self.draw()
        for body in self.plnt:
            s = '{:<8}  Pos.={:>6.2f} {:>6.2f} Vel.={:>10.3f} {:>10.3f}'.format(
                body.name, body.pos[0], body.pos[1], body.v[0], body.v[1])
            print(s)
        print()


earth = Planet([-1, 0], BLUE, "Earth", 10, 10**16, [500, 400])
mars = Planet([0, 1], RED, "Mars", 10, 10**15, [800, 300])
w = World([earth, mars])

while 1:
    screen.fill(BLACK)

    w.update()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_ESCAPE) or (event.type == pygame.QUIT):
                pygame.quit()

    pygame.display.update()
    clock.tick(60)