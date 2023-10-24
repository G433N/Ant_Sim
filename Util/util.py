from math import cos, pi, sin, sqrt
from random import random
from pygame import Vector2

from Util.globals import WORLD_SIZE


def random_vector(bounding_box: Vector2) -> Vector2:
    """
    Get a random non-uniform Vector2 inside the bounding_box
    """
    x = bounding_box.x * random()
    y = bounding_box.y * random()
    return Vector2(x, y)


def rotate_normal(norm_dir: Vector2, rotation_vector: Vector2):
    """rotates the first vector by the second (both needs to be normalized)"""
    return Vector2(
        norm_dir.x * rotation_vector.x - norm_dir.y * rotation_vector.y,
        norm_dir.y * rotation_vector.x + norm_dir.x * rotation_vector.y
    )


def bounds(position: Vector2):
    x, y = position
    max_x, max_y = WORLD_SIZE

    return 0 <= x and x <= max_x and 0 <= y and y <= max_y


def random_vector_disc(radius: float):
    # https://rh8liuqy.github.io/Uniform_Disk.html
    r1, r2 = random(), random()  # type: ignore # Very not uniform but what ever
    return Vector2(
        radius * sqrt(r2) * cos(2 * pi * r1),
        radius * sqrt(r2) * sin(2 * pi * r1)
    )


def random_normal_vector():
    # https://rh8liuqy.github.io/Uniform_Disk.html
    r1 = random()
    return Vector2(
        cos(2 * pi * r1),
        sin(2 * pi * r1)
    )
