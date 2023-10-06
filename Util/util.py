import random
from pygame import Vector2


def random_vector(bounding_box: Vector2) -> Vector2:
    """
    Get a random non-uniform Vector2 inside the bounding_box
    """
    x = bounding_box.x * random.random()
    y = bounding_box.y * random.random()
    return Vector2(x, y)
