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
n = 1
TPS = 60
FPS = 20
draw_time: float = 1 / FPS
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_g:
                show_chunk = not show_chunk
            elif event.key == pygame.K_u:
                draw_time = 1/FPS

    pheromones.update(dt)
    ants.update(dt)
    nests.update(dt)

    if draw_time >= 1/FPS:
        screen.fill(pygame.Color(0, 120, 50))

        pheromones.draw(screen)
        nests.draw(screen)
        food.draw(screen)
        ants.draw(screen)
        if show_chunk:
            ChunkedData.draw(screen)

        pygame.display.flip()
        draw_time = draw_time % 1/FPS

    dt = clock.tick(TPS) / 1000  # limits FPS to 60
    draw_time += dt
    if n == 2000:
        break
        pass
        # print(len(ants.position), clock.get_fps())
    n += 1

pygame.quit()
