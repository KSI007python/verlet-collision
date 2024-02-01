import pygame
import math
import random

screen = pygame.display.set_mode((500, 500))

friction = 0.9999

running = True

mouseClick = False

def find_angle(p1, p2):
    dy = p1[1] - p2[1]
    dx = p1[0] - p2[0]

    if dx == 0 and dy <= 0:
        return math.pi/2
    if dx == 0 and dy >= 0:
        return 3*math.pi/2
    angle = math.atan(dy/dx)
    if dx > 0:
        angle += math.pi
    return angle


class particle:

    def __init__(self, pos, mass, radius, color):
        self.x, self.y = pos
        self.mass = mass
        self.radius = radius
        self.color = color
        self.oldX = self.x
        self.oldY = self.y

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def process(self):
        vX = self.x - self.oldX
        vY = self.y - self.oldY
        self.oldX = self.x
        self.oldY = self.y
        self.x += vX*friction
        self.y += vY*friction

e = 0.5

def set_constraints(p):
    vX = p.x - p.oldX
    vY = p.y - p.oldY
    if p.x < 0:
        p.x = 0
        p.oldX = p.x + vX*e
    if p.x > 500:
        p.x = 500
        p.oldX = p.x + vX*e
    if p.y < 0:
        p.y = 0
        p.oldY = p.y + vY*e
    if p.y > 500:
        p.y = 500
        p.oldY = p.y + vY*e

def collision(p1, p2):
    d = math.sqrt((p1.x-p2.x)**2 + (p1.y-p2.y)**2)
    if d < p1.radius + p2.radius:
        t = find_angle((p1.x, p1.y), (p2.x, p2.y))
        # p1.x -= (p1.radius + p2.radius - d)*math.cos(t)/2
        # p1.y -= (p1.radius + p2.radius - d)*math.sin(t)/2
        # p2.x += (p1.radius + p2.radius - d)*math.cos(t)/2
        # p2.y += (p1.radius + p2.radius - d)*math.sin(t)/2
        v1X = p1.x - p1.oldX
        v1Y = p1.y - p1.oldY
        v2X = p2.x - p2.oldX
        v2Y = p2.y - p2.oldY
        v_rel = math.sqrt((v1X-v2X)**2 + (v1Y-v2Y)**2)
        I = -v_rel*(1+e)/(1/p1.mass + 1/p2.mass)
        p1.oldX -= I*math.cos(t)/p1.mass
        p1.oldY -= I*math.sin(t)/p1.mass
        p2.oldX += I*math.cos(t)/p2.mass
        p2.oldY += I*math.sin(t)/p2.mass

def set_constraints(p):
    vX = p.x - p.oldX
    vY = p.y - p.oldY
    if p.x < 0:
        p.x = 0
        p.oldX = p.x + vX*e
    if p.x > 500:
        p.x = 500
        p.oldX = p.x + vX*e
    if p.y < 0:
        p.y = 0
        p.oldY = p.y + vY*e
    if p.y > 500:
        p.y = 500
        p.oldY = p.y + vY*e

distance = lambda p1, p2 : math.sqrt((p2.x - p1.x)**2 + (p2.y - p1.y)**2)

particles = []

for i in range(5):
    particles.append(particle((random.randint(100, 400), random.randint(100, 400)), 10, 10, (255, 255, 255)))
    t = random.random()*2*math.pi
    particles[i].oldX -= math.cos(t)*0.1
    particles[i].oldY -= math.sin(t)*0.1


def iterate():
    for i in range(len(particles)):
        p = particles[i]
        p.process()
        p.draw()
        p.y += 0.001
        set_constraints(p)
        for j in range(len(particles)):
            if i != j:
                collision(p, particles[j])

while running:
    screen.fill((0, 0, 0))

    iterate()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()