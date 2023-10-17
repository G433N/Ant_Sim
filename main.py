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
font = pygame.font.SysFont("Arial", 18, bold=True)

mouse_position = pygame.Vector2()
pheromones = Pheromone_Grid()
ants = SimpleAnts(pheromones.add)
nests = AntNets(WORLD_SIZE, ants.add)
nests.add(Vector2(900, 300))


food = Food()
food.add(WORLD_SIZE/4, 20, 100)
food.add(Vector2(100, 500), 20, 100)
food.add(WORLD_SIZE/4 + Vector2(700, 0), 20, 100)
food.add(3 * WORLD_SIZE/4, 20, 100)
ants.food = food

show_chunk = False
show_fps = True
show_pheromones = True
show_ant = True
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
            elif event.key == pygame.K_f:
                show_fps = not show_fps
            elif event.key == pygame.K_p:
                show_pheromones = not show_pheromones
            elif event.key == pygame.K_a:
                show_ant = not show_ant

    pheromones.update(dt)
    ants.update(dt)
    nests.update(dt)

    if draw_time >= 1/FPS:

        if show_pheromones:
            screen.blit(pheromones.draw(), (0, 0))
        else:
            screen.fill(pygame.Color(0, 120, 50))

        if show_ant:
            nests.draw(screen)
            food.draw(screen)
            ants.draw(screen)

        if show_chunk:
            ChunkedData.draw(screen)

        if show_fps:
            fps = str(int(clock.get_fps()))
            fps_t = font.render(fps, 1, "RED")
            screen.blit(fps_t, (0, 0))

        pygame.display.flip()
        draw_time = draw_time % 1/FPS

    dt = clock.tick(TPS) / 1000  # limits FPS to 60
    draw_time += dt
    if n == -1000:
        break
    n += 1

pygame.quit()
