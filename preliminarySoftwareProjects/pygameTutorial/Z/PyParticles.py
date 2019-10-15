import random
import math

background_colour = (255,255,255)
(width, height) = (400, 400)
mass_of_air = 0.2
drag = 0.9999
elasticity = 0.75
gravity = (math.pi, 0.01)

def addVectors(vector1, vector2):
    angle1,length1 = vector1
    angle2,length2 = vector2
    x  = math.sin(angle1) * length1 + math.sin(angle2) * length2
    y  = math.cos(angle1) * length1 + math.cos(angle2) * length2

    length = math.hypot(x, y)
    angle = 0.5 * math.pi - math.atan2(y, x)

    return (angle, length)

def findParticle(particles, x, y):
    for p in particles:
        if math.hypot(p.x-x, p.y-y) <= p.size:
            return p
    return None

def collide(p1, p2):
    dx = p1.x - p2.x
    dy = p1.y - p2.y

    dist = math.hypot(dx, dy)
    if dist < p1.size + p2.size:
           angle = math.atan2(dy, dx) + 0.5 * math.pi
           total_mass = p1.mass + p2.mass

           (p1.angle, p1.speed) = addVectors((p1.angle, p1.speed*(p1.mass-p2.mass)/total_mass), (angle, 2*p2.speed*p2.mass/total_mass))
           (p2.angle, p2.speed) = addVectors((p2.angle, p2.speed*(p2.mass-p1.mass)/total_mass), (angle+math.pi, 2*p1.speed*p1.mass/total_mass))
           p1.speed *= elasticity
           p2.speed *= elasticity

           overlap = 0.5* (p1.size + p2.size - dist + 1)
           p1.x += math.sin(angle)*overlap
           p1.y -= math.cos(angle)*overlap
           p2.x -= math.sin(angle)*overlap
           p2.y += math.cos(angle)*overlap

class Particle:
    def __init__(self, position, size, mass=1):
        self.x, self.y = position
        self.size = size
        self.mass = mass
        self.colour = (0, 0, 255)
        self.thickness = 1

        self.speed = 0
        self.angle = 0
        self.drag = (self.mass/(self.mass + mass_of_air)) ** self.size

    def display(self):
        pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.size, self.thickness)

    def move(self):
       # (self.angle, self.speed) = addVectors((self.angle, self.speed), gravity)
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed
        self.speed *= self.drag

    def mouseMove(self, x, y):
        dx = x - self.x
        dy = y - self.y
        self.angle = 0.5*math.pi + math.atan2(dy, dx)
        self.speed = math.hypot(dx, dy) * 0.1

class Environment:
    def __init__(self, screensize):
        width, height = screensize

        self.width = width
        self.height = height
        self.particles = []
        
        self.colour = (255,255,255)
        self.mass_of_air = 0.2
        self.elasticity = 0.75
        self.acceleration = None
        
    def addParticles(self, n=1, **kargs):
        for i in range(n):
            size = kargs.get('size', random.randint(10, 20))
            mass = kargs.get('mass', random.randint(100, 10000))
            x = kargs.get('x', random.uniform(size, self.width - size))
            y = kargs.get('y', random.uniform(size, self.height - size))

            particle = Particle((x, y), size, mass)
            particle.speed = kargs.get('speed', random.random())
            particle.angle = kargs.get('angle', random.uniform(0, math.pi*2))
            particle.colour = kargs.get('colour', (0, 0, 255))
            particle.drag = (particle.mass/(particle.mass + self.mass_of_air)) ** particle.size

            self.particles.append(particle)

    def update(self):
        for i, particle in enumerate(self.particles):
            particle.move()
            if self.acceleration:
                particle.accelerate(self.acceleration)
            self.bounce(particle)
            for particle2 in self.particles[i+1:]:
                collide(particle, particle2)

    def bounce(self, particle):
       if particle.x > self.width - particle.size:
            particle.x = 2 * (width - particle.size) - particle.x
            particle.angle = - particle.angle
            partcile.speed *= self.elasticity

       elif particle.x < particle.size:
            particle.x = 2 * particle.size - particle.x
            particle.angle = - particle.angle
            particle.speed *= self.elasticity

       if particle.y > self.height - particle.size:
            particle.y = 2 * (self.height - particle.size) - particle.y
            particle.angle = math.pi - particle.angle
            particle.speed *= self.elasticity

       elif particle.y < particle.size:
            particle.y = 2 * particle.size - particle.y
            particle.angle = math.pi - particle.angle
            particle.speed *= self.elasticity

    def findParticle(self, x, y):
        for particle in self.particles:
            if math.hypot(particle.x - x, particle.y - y) <= particle.size:
                return particle
        return None





