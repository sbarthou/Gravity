import pygame
import numpy as np
from sys import exit


pygame.init()
size = WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode(size)
pygame.display.set_caption('2-Body')
clock = pygame.time.Clock()


# constantes
CENTER = (WIDTH/2, HEIGHT/2)
G = 0.001  # Ajusta este valor según sea necesario
dt = 0
s = 0
font = pygame.font.SysFont ("Apple Symbols", 20)  # Crea un objeto de fuente


class Body:
    def __init__(self, path, m, x_pos, y_pos):
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect()
        self.rect.center = (x_pos, y_pos)
        self.m = m
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.vx = 0
        self.vy = 0

    def position(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect.center = (self.x_pos, self.y_pos)

    def gravitate(self, body1, dt):
        r = np.sqrt((self.x_pos - body1.x_pos)**2 + (self.y_pos - body1.y_pos)**2)   # r: distancia entre body1 y body2
        theta = np.arctan2((body1.y_pos - self.y_pos), (body1.x_pos - self.x_pos))   # theta: angulo entre body1 y body2
        F = G * ((self.m * body1.m) / r**2)   # fuerza gravitacional de body1 sobre body2
        Fx = F * np.cos(theta)   # componente x de la fuerza gravitacional
        Fy = F * np.sin(theta)   # componente y de la fuerza gravitacional
        ax = Fx / self.m   # componente x de la aceleración
        ay = Fy / self.m   # componente x de la aceleración

        # Actualizar las componentes de velocidad
        self.vx += ax * dt
        self.vy += ay * dt

        # Actualizar la posición en función de la velocidad
        self.x_pos += self.vx * dt
        self.y_pos += self.vy * dt
        self.position(self.x_pos, self.y_pos)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


body1 = Body('assets/circle25px.png', 100, WIDTH/2, HEIGHT/2)
body2 = Body('assets/circle5px.png', 10, 0, 0)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill('black')

    body2.gravitate(body1, dt)
    body1.draw(screen)
    body2.draw(screen)
    dt += 0.1  # Paso de tiempo para la integración
    
    # Renderiza el tiempo en la pantalla
    time_text = font.render(f'{round(dt, 3)} s', True, (255, 255, 255))
    screen.blit(time_text, (WIDTH/2, 10))  # Ubicación del texto en pantalla

    pygame.display.flip()
    clock.tick(60)