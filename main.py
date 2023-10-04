import pygame
from ant import Ant
from ant_nest import AntNest
from movment import Movment, friction, update_movement
from pygame import Vector2, draw
from util import random_vector

from world import WorldObject

SCREENSIZE = (1280, 720)
WORLDSIZE = Vector2(SCREENSIZE)

pygame.init()

screen = pygame.display.set_mode(SCREENSIZE)
clock = pygame.time.Clock()
dt: float = 0
running = True

objects: list[WorldObject] = list()

# for _ in range(100):
#    objects.append(Ant(Vector2(), random_vector(WORLDSIZE)))
objects.append(AntNest(Vector2(500, 500)))
# objects.append(AntNest(Vector2(100, 700)))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("darkgreen")

    for obj in objects:

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

        draw.circle(screen, obj.color, obj.position, obj.radius)

    pygame.display.flip()
    dt = clock.tick(60) / 1000  # limits FPS to 60
pygame.quit()