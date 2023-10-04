import random
from pygame import Surface, Vector2, draw

from ECS.world_object import WorldObject



def draw_objects(screen: Surface, obj: WorldObject, dt: float):
    draw.circle(screen, obj.color, obj.position, obj.radius)


def random_vector(space: Vector2) -> Vector2:
    x = space.x * random.random()
    y = space.y * random.random()
    return Vector2(x, y)
