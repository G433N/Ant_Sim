import pygame
from functools import partial
from ECS.world_generator import WorldGenerator
from Objects.Componets.world_object import WorldObject
from Objects.ant import Ant, ant_system
from Objects.ant_nest import AntNest, ant_nest_system
from pygame import Vector2
from Objects.Componets.movment import Movment, movement_system
from util import draw_system

SCREENSIZE = (1280, 720)
WORLDSIZE = Vector2(SCREENSIZE)

pygame.init()
screen = pygame.display.set_mode(SCREENSIZE)
clock = pygame.time.Clock()
dt: float = 0
running = True

setup = WorldGenerator()
setup.add_system(AntNest, partial(ant_nest_system, WORLDSIZE))
setup.add_system(Ant, partial(ant_system, WORLDSIZE))
setup.add_system(Movment, movement_system)
setup.add_system(WorldObject, partial(draw_system, screen))

world = setup.compile()
world.spawn(AntNest(Vector2(500, 500)))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("darkgreen")
    world.run(dt)

    pygame.display.flip()
    dt = clock.tick(60) / 1000  # limits FPS to 60
pygame.quit()
