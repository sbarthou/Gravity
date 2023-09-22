import pygame
import itertools
import numpy as np
from sys import exit


pygame.init()

# Obtener las dimensiones de la pantalla
screen_info = pygame.display.Info()
WIDTH = screen_info.current_w
HEIGHT = screen_info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption('n-Body')
clock = pygame.time.Clock()
font = pygame.font.SysFont ("Apple Symbols", 15)


# constantes
CENTER = (WIDTH/2, HEIGHT/2)
G = 0.1
e = 1.5
dt = 0.1


class Body:
    def __init__(self, radius, mass, x=0, y=0, vX=0, vY=0):
        self.radius = radius
        self.mass = mass
        self.x = x
        self.y = y
        self.vX = vX
        self.vY = vY
        
    def gravitate(self, body, dt):
        r = np.sqrt((self.x - body.x)**2 + (self.y - body.y)**2)
        theta = np.arctan2((body.y - self.y), (body.x - self.x))
        F = G * ((self.mass * body.mass) / (r + e)**2)
        Fx = F * np.cos(theta)
        Fy = F * np.sin(theta)
        
        aX = Fx / self.mass
        aY = Fy / self.mass
        
        self.vX += aX * dt
        self.vY += aY * dt
        
        self.x += self.vX * dt
        self.y += self.vY * dt
        
        # self.x += self.vX * dt + (1/2) * aX * dt**2
        # self.y += self.vY * dt + (1/2) * aY * dt**2
    
    def draw(self, screen):
        pygame.draw.rect(screen, '#FFFFFF', (self.x, self.y, self.radius, self.radius))
        
    
N = 50   
bodies = []
for i in range(N):
    x = np.random.randint(WIDTH)
    y = np.random.randint(HEIGHT)
    bodies.append(Body(2, 5, x, y))


body_pairs = []

for i in range(len(bodies)):
    for j in range(len(bodies)):
        if i != j:
            pair = (bodies[i], bodies[j])
            body_pairs.append(pair)

    
fps = 0
frame_count = 0
last_time = pygame.time.get_ticks()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill('black')

    for body1, body2 in body_pairs:
        body1.gravitate(body2, dt)
        body2.gravitate(body1, dt)
        body1.draw(screen)
        body2.draw(screen)
    
    # FPS
    frame_count += 1
    if pygame.time.get_ticks() - last_time >= 1000:  # Update every second
        fps = frame_count
        frame_count = 0
        last_time = pygame.time.get_ticks()
    # Render FPS
    fps_text = font.render(f'FPS: {fps}', True, '#FFEA00')
    screen.blit(fps_text, (0, 0))

    pygame.display.flip()
    clock.tick(60)