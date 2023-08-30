# carga imagen | matriz de imágenes | rotar imágenes

import pygame
import numpy as np
from sys import exit


class Vectors:
    def __init__(self, path):
        self.original_vector = pygame.image.load(path)
        self.vector = self.original_vector.copy()
        self.rect = self.vector.get_rect()
        
    def draw_single(self, pos):
        self.rect = self.vector.get_rect(center=(pos))
        screen.blit(self.vector, self.rect.topleft)
        
    def matrix(self, WIDTH, HEIGHT):
        for i in range(25, WIDTH, 25):
            for j in range(25, HEIGHT, 25):
                self.rect = self.vector.get_rect(center=(i, j))
                screen.blit(self.vector, self.rect.topleft)
                
    def rotate(self, angle):
        self.vector = pygame.transform.rotate(self.original_vector, angle)
        
    def point(self, surface):
        pygame.draw.circle(surface, red, (self.rect.centerx, self.rect.top), 3)


pygame.init()
size = WIDTH, HEIGHT = 700, 700
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Gravity')
clock = pygame.time.Clock()


# constantes
CENTER = (WIDTH/2, HEIGHT/2)
white = '#FFFFFF'
black = '#000000'
red = '#FF0000'
blue = '#0000FF'
green = '#00FF00'


vector = Vectors('assets/arrow100px.png')
angle = 0


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
             
    screen.fill(black)
    
    vector.draw_single(CENTER)
    vector.point(screen)
    
    # vector.matrix(WIDTH, HEIGHT)
    # vector.rotate(angle)
    
    angle += 1
    if angle >= 360:
        angle = 0
    
    pygame.display.flip()
    clock.tick(60)