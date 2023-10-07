import pygame
from Ant.Food.food import Food
from Ant.Nest.ant_nests import AntNets
from Ant.Pheromone.pheromones import Pheromones
from Ant.simple_ants import SimpleAnts
from Util.chunks import ChunkedData
from Util.globals import SCREEN_SIZE, WORLD_SIZE
from pygame import mouse, Vector2


pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
dt: float = 0
running = True

mouse_position = pygame.Vector2()
pheromones = Pheromones()
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
    food.draw(screen)
    ants.draw(screen)
    if show_chunk:
        ChunkedData.draw(screen)

    pygame.display.flip()
    dt = clock.tick(60) / 1000  # limits FPS to 60
pygame.quit()
