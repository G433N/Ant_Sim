from typing import Final
import pygame
from pygame import Vector2
from ant_nests import Ant_Nets

from ants import Ants

SCREENSIZE: Final = (1280, 720)
WORLDSIZE: Final = Vector2(SCREENSIZE)

pygame.init()
screen = pygame.display.set_mode(SCREENSIZE)
clock = pygame.time.Clock()
dt: float = 0
running = True

ants = Ants(WORLDSIZE)
ant_nets = Ant_Nets(WORLDSIZE, ants.add)
ant_nets.add(WORLDSIZE / 2)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ant_nets.update(dt)
    ants.update(dt)
    screen.fill("darkgreen")
    ant_nets.draw(screen)
    ants.draw(screen)

    pygame.display.flip()
    dt = clock.tick(60) / 1000  # limits FPS to 60
pygame.quit()
