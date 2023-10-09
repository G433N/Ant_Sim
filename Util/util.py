import random
from pygame import Vector2

from Util.globals import WORLD_SIZE


def random_vector(bounding_box: Vector2) -> Vector2:
    """
    Get a random non-uniform Vector2 inside the bounding_box
    """
    x = bounding_box.x * random.random()
    y = bounding_box.y * random.random()
    return Vector2(x, y)


def bounds(position: Vector2):
    x, y = position
    max_x, max_y = WORLD_SIZE

    return 0 <= x and x <= max_x and 0 <= y and y <= max_y
