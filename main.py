import pygame
from Ant.Nest.ant_nests import AntNets
from Ant.ants import Ants
from Util.globals import SCREEN_SIZE, WORLD_SIZE
from Ant.Pheromone.pheromones import Pheromones


pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
dt: float = 0
running = True

pheromones = Pheromones()
pheromones.add(WORLD_SIZE / 3)
ants = Ants(WORLD_SIZE, pheromones.add)
ant_nets = AntNets(WORLD_SIZE, ants.add)
ant_nets.add(WORLD_SIZE / 2)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pheromones.update(dt)
    ant_nets.update(dt)
    ants.update(dt)

    screen.fill("darkgreen")

    pheromones.draw(screen)
    ant_nets.draw(screen)
    ants.draw(screen)

    pygame.display.flip()
    dt = clock.tick(60) / 1000  # limits FPS to 60
pygame.quit()
