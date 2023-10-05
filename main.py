from typing import Final
import pygame
from pygame import Vector2
from ant_nests import AntNets

from ants import Ants
from pheromones import Pheromones

SCREEN_SIZE: Final = (1280, 720)
WORLD_SIZE: Final = Vector2(SCREEN_SIZE)
if __name__ == "__main__":
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
