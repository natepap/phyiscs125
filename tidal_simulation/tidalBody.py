from turtle import *
import math

# The gravitational constant G
G = 6.67428e-11

# Scaling
SCALE = 50000

# Mass of water blocks in kg
WB = 100000

class Planet(Turtle):
    """Subclass of Turtle representing a planet with water
    that can have tides that depend on gravitational forces of other bodies

    mass = mass in kg
    bodylist = list of other gravitational bodies
    equi = equilibrium height of ocean
    dh = change in tidal height due to gravity
    diam = diameter of the planet
    water_list = water on the planet
    """

    name = 'Planet'
    mass = None
    equi = None
    dh = None
    bodylist = None
    diam = None
    water_list = []

    def equi_force(self):
        """gives the gravitational force of the planet"""
        return G * self.mass * WB/ (self.diam ** 2)

    def setup(self):
        for x in range(720):

            #creates water pixels every half degree around the planet at the equilibrium height
            water = None
            water.px = (self.diam + self.equi) * math.cos(x/2)
            water.py = (self.diam + self.equi) * math.sin(x/2)

            water = self.dot(3, 'blue')
            self.water_list.append(water)

    def tide_force_sum(self, bodylist):
        """Returns the sum of gravitational forces of other bodies"""

        for body in bodylist:
            # Don't include the planet as its force
            if self is body:
                continue

            for water in self.water_list:
                dx = (body.px - water.px)
                dy = (body.py - water.py)

                d = math.sqrt(water.px**2 + water.py**2)

                dr = math.sqrt(dx**2 + dy**2)

                if dr == 0:
                    raise ValueError("Collision between objects %r and %r"
                                     % (self.name, body.name))

                f_tid = G * body.mass * WB / (dr**2)
                f_g = G * body.mass * WB / (d**2)

                theta = math.atan2(dy, dx)
                fx = math.cos(theta) * f_tid - f_g
                fy = math.sin(theta) * f_tid - f_g

                return fx, fy

    def ref_frame_force(self, bodylist):
        """Returns the force of acceleration due to the reference frame of the planet
        being noninertial"""

        for body in bodylist:

            if self is body:
                continue

            dx = (self.px - body.px)
            dy = (self.py - body.py)

            d = math.sqrt(dx**2 + dy**2)

            if d == 0:
                raise ValueError("Collision between objects %r and %r"
                                 % (self.name, body.name))

            f = G * body.mass * WB / (d**2)

            theta = math.atan2(dy, dx)
            fx = math.cos(theta) * f
            fy = math.sin(theta) * f

            return fx, fy

def update_info(step, bodies):
   """(int, [Body])

   Displays information about the status of the simulation.
   """
   print('Step #{}'.format(step))
   for body in bodies:
       s = '{:<8}  Pos.={:>6.2f} {:>6.2f}'.format(
           body.name, body.px / SCALE, body.py / SCALE)
   print(s)
   print()

def loop(bodies):
   """([Body])
   Never returns; loops through the simulation, updating the
   positions of all the provided bodies.
   """
   timestep = 24 * 3600  # One day

   for body in bodies:
       body.penup()
       body.hideturtle()

   step = 1
   while True:
       update_info(step, bodies)
       step += 1

   force = {}
   for body in bodies:
       # Add up all of the forces exerted on 'body'.
       total_fx = total_fy = 0.0
       for other in bodies:
            # Don't calculate the body's attraction to itself
            if body is other:
                  continue
            fx, fy = body.attraction(other)
            total_fx += fx
            total_fy += fy

            # Record the total force exerted.
            force[body] = (total_fx, total_fy)

       # Update velocities based upon on the force.
       for body in bodies:
            fx, fy = force[body]
            body.vx += fx / body.mass * timestep
            body.vy += fy / body.mass * timestep

            # Update positions
            body.px += body.vx * timestep
            body.py += body.vy * timestep
            body.clearstamps()
            body.goto(body.px * SCALE, body.py * SCALE)
            body.showturtle()
            body.pendown()