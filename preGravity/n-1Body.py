import pygame
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


# constantes
CENTER = (WIDTH/2, HEIGHT/2)
G = 0.001
dt = 0
font = pygame.font.SysFont ("Apple Symbols", 15)


class Body:
    def __init__(self, path, m, posX, posY):
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect()
        self.rect.center = (posX, posY)
        self.m = m
        self.posX = posX
        self.posY = posY
        self.vx = 0
        self.vy = 0
        
    def position(self, posX, posY):
        self.posX = posX
        self.posY = posY
        self.rect.center = (posX, posY)
        
    def gravitate(self, body1, dt):
        r = np.sqrt((self.posX - body1.posX)**2 + (self.posY - body1.posY)**2)
        theta = np.arctan2((body1.posY - self.posY), (body1.posX - self.posX))
        F = G * ((self.m * body1.m) / r**2)
        Fx = F * np.cos(theta)
        Fy = F * np.sin(theta)
        ax = Fx / self.m 
        ay = Fy / self.m
        
        self.vx += ax * dt
        self.vy += ay * dt
        
        self.posX += self.vx * dt
        self.posY += self.vy * dt
        self.position(self.posX, self.posY)
        
    def collide(self, bodies, body, body1):
        x = body1.posX
        y = body1.posY
        r = 10
        if (self.posX >= x-r and self.posX <= x+r) and ((self.posY >= y-r and self.posY <= y+r)):
            bodies.remove(body)
            
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        
       
def generate_bodies(m, n):
    bodies = []
    for i in range(n):
        x = np.random.randint(WIDTH)
        y = np.random.randint(HEIGHT)
        body = Body('assets/circle2px.png', m, x, y)
        bodies.append(body)
    return bodies
        
        
bodies = generate_bodies(1, 10000)
body1 = Body('assets/circle25px.png', 10, WIDTH/2, HEIGHT/2)
        

# Variables for FPS display
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

    body1.draw(screen)
    
    for body in bodies:
        body.gravitate(body1, dt)
        body.draw(screen)
        body.collide(bodies, body, body1)
    
    dt += 0.1
    dt_text = font.render(f'{round(dt, 2)} s', True, '#FFEA00')
    screen.blit(dt_text, (WIDTH - dt_text.get_width(), 0))
    
    # Calculate FPS
    frame_count += 1
    if pygame.time.get_ticks() - last_time >= 1000:  # Update every second
        fps = frame_count
        frame_count = 0
        last_time = pygame.time.get_ticks()
    # Render FPS text
    fps_text = font.render(f'FPS: {fps}', True, '#FFEA00')
    screen.blit(fps_text, (0, 0))

    pygame.display.flip()
    clock.tick(60)