from functools import partial
import pygame
from ant import Ant, update_ant
from ant_nest import AntNest, update_ant_nest
from pygame import Vector2, draw
from movment import Movment, update_movement
from world import World

SCREENSIZE = (1280, 720)
WORLDSIZE = Vector2(SCREENSIZE)

pygame.init()

screen = pygame.display.set_mode(SCREENSIZE)
clock = pygame.time.Clock()
dt: float = 0
running = True

world = World()

world.add_system(AntNest, partial(update_ant_nest, WORLDSIZE))
world.add_system(Ant, partial(update_ant, WORLDSIZE))
world.add_system(Movment, update_movement)

world.add_object(AntNest(Vector2(500, 500)))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("darkgreen")
    world.run(dt)

    for obj in world.get_objects():
        draw.circle(screen, obj.color, obj.position, obj.radius)

    pygame.display.flip()
    dt = clock.tick(60) / 1000  # limits FPS to 60
pygame.quit()

"""
        if isinstance(obj, Movment):
            friction(obj)
            update_movement(obj, dt)

        if isinstance(obj, Ant):
            if obj.position.distance_squared_to(obj.target) < 100:
                obj.target = random_vector(WORLDSIZE)

            dir = (obj.target - obj.position).normalize()
            obj.acceleration = dir * 150
            #draw.circle(screen, "yellow", obj.target, 5)

        if isinstance(obj, AntNest):
            obj.timer += dt
            if obj.spawmed < obj.spawn and obj.timer > obj.time:
                objects.append(
                    Ant(obj.position.copy(), random_vector(WORLDSIZE)))
                obj.timer = obj.timer % obj.time
                obj.spawmed += 1
"""
