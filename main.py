import pygame
from Ant.Nest.ant_nests import AntNets
from Ant.Pheromone.pheromones import Pheromones
from Ant.simple_ants import SimpleAnts
from Util.chunks import Chunks
from Util.globals import SCREEN_SIZE, WORLD_SIZE
from pygame import mouse


pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
dt: float = 0
running = True

mouse_position = pygame.Vector2()
pheromones = Pheromones()
ants = SimpleAnts(WORLD_SIZE, pheromones.add)
nests = AntNets(WORLD_SIZE, ants.add)
nests.add(WORLD_SIZE / 2)

test_chunk = Chunks(WORLD_SIZE)
show_chunk = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_g:
                show_chunk = not show_chunk

    mouse_position.x, mouse_position.y = mouse.get_pos()

    pheromones.update(dt)
    ants.update(dt)
    nests.update(dt)

    screen.fill("darkgreen")

    pheromones.draw(screen)
    nests.draw(screen)
    ants.draw(screen)
    if show_chunk:
        test_chunk.draw(screen)

    pygame.display.flip()
    dt = clock.tick(60) / 1000  # limits FPS to 60
pygame.quit()
