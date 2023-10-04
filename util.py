import random
from pygame import Vector2


def random_vector(space: Vector2) -> Vector2:
    x = space.x * random.random()
    y = space.y * random.random()
    return Vector2(x, y)
