import pygame
from Ant.Nest.ant_nests import AntNets
from Ant.ants import Ants
from Ant.Pheromone.pheromone_grid import Pheromone_Grid
from Util.globals import SCREEN_SIZE, WORLD_SIZE


pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
dt: float = 0
running = True

pheromones = Pheromone_Grid()
ants = Ants(WORLD_SIZE, pheromones.add)
ant_nets = AntNets(WORLD_SIZE, ants.add)
ant_nets.add(pygame.Vector2(WORLD_SIZE/2))

n = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    pheromones.update(dt)
    ant_nets.update(dt)
    ants.update(dt)

    screen.fill(pygame.Color(0, 120, 50))

    # pheromones.draw(screen)
    ant_nets.draw(screen)
    ants.draw(screen)

    pygame.display.flip()
    dt = clock.tick(120) / 1000  # limits FPS to 60
    if n % 60 == 0:
        print(len(ants.position), clock.get_fps())
    n += 1
    
pygame.quit()
