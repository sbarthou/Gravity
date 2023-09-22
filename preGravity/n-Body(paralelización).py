import pygame
import multiprocessing
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
        self.aX = 0
        self.aY = 0
        
    def gravitate(self, body, dt):
        r = np.sqrt((self.x - body.x)**2 + (self.y - body.y)**2)
        theta = np.arctan2((body.y - self.y), (body.x - self.x))
        F = G * ((self.mass * body.mass) / (r + e)**2)
        Fx = F * np.cos(theta)
        Fy = F * np.sin(theta)
        
        self.aX = Fx / self.mass
        self.aY = Fy / self.mass
        
        self.vX += self.aX * dt
        self.vY += self.aY * dt
        
        self.x += self.vX * dt
        self.y += self.vY * dt
    
    def draw(self, screen):
        pygame.draw.rect(screen, '#FFFFFF', (self.x, self.y, self.radius, self.radius))


N = 100   
bodies = []
for i in range(N):
    x = np.random.randint(WIDTH)
    y = np.random.randint(HEIGHT)
    bodies.append(Body(2, 10, x, y))
    
# Función para calcular interacciones entre un subconjunto de partículas
def calculate_interactions(start_idx, end_idx, bodies, dt):
    for i in range(start_idx, end_idx):
        for j in range(len(bodies)):
            if i != j:
                bodies[i].gravitate(bodies[j], dt)

# Dividir el trabajo entre múltiples procesos
num_cores = multiprocessing.cpu_count()
chunk_size = len(bodies) // num_cores
processes = []
for i in range(num_cores):
    start_idx = i * chunk_size
    end_idx = (i + 1) * chunk_size if i < num_cores - 1 else len(bodies)
    process = multiprocessing.Process(target=calculate_interactions, args=(start_idx, end_idx, bodies, dt))
    processes.append(process)

# Iniciar los procesos
for process in processes:
    process.start()

    
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
    
    # Esperar a que todos los procesos terminen
    for process in processes:
        process.join()

    for body in bodies:
        # Calcular la nueva posición y velocidad
        body.x += body.vX * dt + 0.5 * body.aX * dt**2
        body.y +=  body.vY * dt + 0.5 * body.aY * dt**2
        body.vX += body.aX * dt
        body.vY += body.aY * dt

        # Calcular la aceleración para el próximo paso de tiempo
        body.aX = 0
        body.aY = 0
        for other_body in bodies:
            if body != other_body:
                body.gravitate(other_body, dt)
                
        body.draw(screen)
    
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