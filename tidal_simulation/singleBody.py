import pygame
from pygame import *
import math

pygame.init()

screen = pygame.display.set_mode([0, 0], pygame.FULLSCREEN)
clock = pygame.time.Clock()

width = screen.get_width()
height = screen.get_height()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (128, 128, 128)
YELLOW = (255, 255, 0)

# The gravitational constant G
G = 6.67428e-11

# Mass of water - particle
M = 10000

# Scale of orbits
SCALE = 10000000

class Planet():
    def __init__(self, mass = 1, diameter = 1, color = BLACK):
        self.mass = mass
        self.diam = diameter
        self.color = color
        self.water_list = []

    def accel(self):
        return G * self.mass / ((self.diam / 2) ** 2)

    def setup(self):

        pygame.draw.circle(screen, self.color, [math.ceil(width / 2), math.ceil(height / 2)], math.ceil(self.diam / 2), 0)

        for i in range(0, 360, 3):
            j = i * math.pi / 180

            dx = math.cos(j) * self.diam / 2
            dy = math.sin(j) * self.diam / 2

            water = pygame.draw.circle(screen, BLUE, [math.ceil(width/2 + dx), math.ceil(height/2 + dy)], 1)
            sublist = [water, [math.ceil(width/2 + dx), math.ceil(height/2 + dy)], [0, 0]]
            self.water_list.append(sublist)

    def update(self):
        for water in self.water_list:
            print(self.accel())
            print(water[2][0], water[2][1], "*")
            hx = self.accel() - water[2][0] - 5*10**27
            hy = self.accel() - water[2][1] - 10**26

            print(hx, hy)
            height_factor = 5 * 10**-27

            water[0] = pygame.draw.circle(screen, BLUE,
                                          [math.ceil(water[1][0] - hx * height_factor),
                                           math.ceil(water[1][1] - hy * height_factor)], 1)

            water[2][0] = water[2][1] = 0

class Moon():
    def __init__(self, mass = 1, diameter = 10, color = BLACK, planet = None, pos = [300,300], vel = [1,1]):
        self.mass = mass
        self.diam = diameter
        self.color = color
        self.planet = planet
        self.pos = pos[:]
        self.v = vel[:]

    def update(self):

        self.pos[0] += self.v[0]
        self.pos[1] += self.v[1]

        pygame.draw.circle(screen, self.color, [math.ceil(self.pos[0]), math.ceil(self.pos[1])],
                           math.ceil(self.diam / 2), 0)

    def orbit(self):

        dx = self.pos[0] - (width / 2)
        dy = self.pos[1] - (height / 2)
        d = math.sqrt(dx ** 2 + dy ** 2)

        if d == 0:
            raise ValueError("Collision between objects %r and %r"
                             % (self.name, self.planet.name))

        f = - G * self.mass * self.planet.mass / (d * SCALE ** 2)

        theta = math.atan2(dy, dx)
        fx = math.cos(theta) * f
        fy = math.sin(theta) * f

        self.v[0] += fx / self.mass
        self.v[1] += fy / self.mass

        self.update()

    def tidal_force(self, list):

        for water in list:

            moon_dir = [water[1][0] - self.pos[0], water[1][1] - self.pos[1]]
            moon_dist = math.sqrt((moon_dir[0])**2 + (moon_dir[1])**2)

            planet_dir = [width - self.pos[0], height - self.pos[1]]
            planet_dist = math.sqrt((planet_dir[0])**2 + (planet_dir[1])**2)

            fx = - G * self.mass * M * (
                        (moon_dir[0] / moon_dist ** 2) - (planet_dir[0] / planet_dist ** 2)) * SCALE**2
            fy = - G * self.mass * M * (
                        (moon_dir[1] / moon_dist ** 2) - (planet_dir[1] / planet_dist ** 2)) * SCALE**2

            water[2][0] += fx
            water[2][1] += fy

earth = Planet(5.97 * 10**24, 100, GRAY)
moon = Moon(0.073 * 10**24, 10, GREEN, earth, [350, (height / 2)], [0, 2])

while 1:
    screen.fill(BLACK)
    earth.setup()
    moon.orbit()
    moon.tidal_force(earth.water_list)
    earth.update()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_ESCAPE) or (event.type == pygame.QUIT):
                pygame.quit()

    pygame.display.update()
    clock.tick(1000)