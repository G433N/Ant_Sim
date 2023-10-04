from functools import partial
import pygame
from ECS.init_world import InitWorld
from ECS.world_object import WorldObject
from ant import Ant, update_ant
from ant_nest import AntNest, update_ant_nest
from pygame import Vector2
from movment import Movment, update_movement
from util import draw_objects

SCREENSIZE = (1280, 720)
WORLDSIZE = Vector2(SCREENSIZE)

pygame.init()
screen = pygame.display.set_mode(SCREENSIZE)
clock = pygame.time.Clock()
dt: float = 0
running = True

world = InitWorld()
world.add_system(AntNest, partial(update_ant_nest, WORLDSIZE))
world.add_system(Ant, partial(update_ant, WORLDSIZE))
world.add_system(Movment, update_movement)
world.add_system(WorldObject, partial(draw_objects, screen))

world = world.compile()
world.add_object(AntNest(Vector2(500, 500)))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("darkgreen")
    world.run(dt)

    pygame.display.flip()
    dt = clock.tick(60) / 1000  # limits FPS to 60
pygame.quit()
