

from pygame import Surface, Vector2, draw

from Util.globals import WORLD_SIZE


CHUNK_SIZE = 100


class ChunkedData[T]:

    _data: dict[int, T]

    def __init__(self) -> None:
        pass

    @classmethod
    def draw(cls, surface: Surface):
        max_x, max_y = WORLD_SIZE.xy
        x, y = 0, 0

        while x < max_x:
            draw.line(surface, "White", Vector2(x, 0), Vector2(x, max_y), 2)
            x += CHUNK_SIZE
        while y < max_y:
            draw.line(surface, "White", Vector2(0, y), Vector2(max_x, y), 2)
            y += CHUNK_SIZE
