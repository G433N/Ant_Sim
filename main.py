import pygame
from Ant.Food.food import Food
from Ant.Nest.ant_nests import AntNets
from Ant.Pheromone.pheromone_grid import Pheromone_Grid
from Ant.simple_ants import SimpleAnts
from Util.chunked_data import ChunkedData
from Util.globals import SCREEN_SIZE, WORLD_SIZE
from pygame import Vector2


pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
dt: float = 0
running = True

mouse_position = pygame.Vector2()
pheromones = Pheromone_Grid()
ants = SimpleAnts(pheromones.add)
nests = AntNets(WORLD_SIZE, ants.add)
nests.add(WORLD_SIZE / 2)

food = Food()
food.add(WORLD_SIZE/4, 20, 100)
food.add(Vector2(100, 500), 20, 100)
food.add(WORLD_SIZE/4 + Vector2(700, 0), 20, 100)
food.add(3 * WORLD_SIZE/4, 20, 100)
ants.food = food

show_chunk = False
n = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_g:
                show_chunk = not show_chunk

    pheromones.update(dt)
    ants.update(dt)
    nests.update(dt)

    screen.fill(pygame.Color(0, 120, 50))

    pheromones.draw(screen)
    nests.draw(screen)
    food.draw(screen)
    ants.draw(screen)
    if show_chunk:
        ChunkedData.draw(screen)

    pygame.display.flip()
    dt = clock.tick(120) / 1000  # limits FPS to 60
    if n % 60 == 0:
        print(len(ants.position), clock.get_fps())
    n += 1

pygame.quit()
