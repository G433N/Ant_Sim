

from pygame import Surface, Vector2, draw


CHUNK_SIZE = 100


class Chunks:

    world_size: Vector2

    def __init__(self, world_size: Vector2) -> None:
        self.world_size = world_size

    def draw(self, surface: Surface):
        max_x, max_y = self.world_size.xy
        x, y = 0, 0

        while x < max_x:
            draw.line(surface, "White", Vector2(x, 0), Vector2(x, max_y), 2)
            x += CHUNK_SIZE
        while y < max_y:
            draw.line(surface, "White", Vector2(0, y), Vector2(max_x, y), 2)
            y += CHUNK_SIZE
