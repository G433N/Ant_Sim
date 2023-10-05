import random
from pygame import Surface, Vector2, draw
from Objects.Componets.world_object import WorldObject


def draw_system(screen: Surface, obj: WorldObject, dt: float):
    draw.circle(screen, obj.color, obj.position, obj.radius)


def random_vector(bounding_box: Vector2) -> Vector2:
    """
    Get a random non-uniform Vector2 inside the bounding_box
    """
    x = bounding_box.x * random.random()
    y = bounding_box.y * random.random()
    return Vector2(x, y)
