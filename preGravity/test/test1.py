# carga imagen | matriz de imágenes | rotar imágenes

import pygame
import numpy as np
from sys import exit


class Vectors:
    def __init__(self, path):
        self.original_vector = pygame.image.load(path)   # cargar imagen original
        self.vector = self.original_vector.copy()   # crear una copia de la imagen original
        self.rect = self.vector.get_rect()   # obtener rectángulo de la imagen
        
    def draw_single(self, x_pos, y_pos):
        self.rect = self.vector.get_rect(center=(x_pos, y_pos))   # actualizar rectángulo al nuevo centro
        screen.blit(self.vector, self.rect.topleft)   # dibujar imagen
        
    # crear matriz
    def matrix(self, WIDTH, HEIGHT):
        for i in range(25, WIDTH, 25):
            for j in range(25, HEIGHT, 25):
                self.rect = self.vector.get_rect(center=(i, j))   # actualizar rectángulo al nuevo centro
                screen.blit(self.vector, self.rect.topleft)   # dibujar imagen
                
    def rotate(self, angle):
        self.vector = pygame.transform.rotate(self.original_vector, angle)   # rotar imagen


pygame.init()
size = WIDTH, HEIGHT = 700, 700
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Gravity')
clock = pygame.time.Clock()

# Creación de objeto Vectors y ángulo de rotación
vector = Vectors('assets/arrow20px.png')
angle = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
             
    screen.fill((0, 0, 0))
    
    vector.matrix(WIDTH, HEIGHT)   # dibujar la matriz de imágenes
    vector.rotate(angle)   # rotar las imágenes
    
    angle += 1
    if angle >= 360:
        angle = 0
    
    pygame.display.flip()
    clock.tick(60)