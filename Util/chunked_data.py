

from typing import Iterable, NamedTuple, Optional, cast
from pygame import Surface, Vector2, draw

from Util.globals import WORLD_SIZE

"""
TODO: make chunks versions of all get chunk methods 
TODO: make values updatable and move chuck
TODO: Maybe make a list for index -> chunk so no need for search
"""

CHUNK_SIZE = 20


def get_neighborhood(x: int):
    return (x-1, x, x+1, -1, 0, 1, -x-1, -x, -x+1)


class Point(NamedTuple):
    x: int
    y: int


class ChunkedData[T]:

    _data: list[Optional[T]]
    chunks: list[set[int]]

    removed_index: set[int]
    dimensions: Point

    def __init__(self, world_size: Vector2) -> None:
        self._data = list()

        self.removed_index = set()

        x, y = world_size // CHUNK_SIZE
        x, y = int(x+1), int(y+1)
        self.dimensions = Point(x, y)
        self.len = x*y
        self.chunks = [set() for _ in range(x*y)]

    def get_chunk_index(self, position: Vector2) -> int:
        x, y = position // CHUNK_SIZE
        x, y = int(x), int(y)
        return x + y * self.dimensions.x

    def add(self, value: T, position: Vector2):
        chunk = self.get_chunk_index(position)
        return self.add_to_chunk(value, chunk)

    def add_to_chunk(self, value: T, chunk: int):
        if len(self.removed_index):
            index = self.removed_index.pop()
            self._data[index] = value
        else:
            index = len(self._data)
            self._data.append(value)

        self.chunks[chunk].add(index)
        return index

    def remove(self, index: int):
        chunk = self.find_chunk(index)
        self._data[index] = None
        self.chunks[chunk].remove(index)
        self.removed_index.add(index)

    def find_chunk(self, index: int):
        for i, s in enumerate(self.chunks):
            if index in s:
                return i
        raise ValueError("Invalid index")

    def enumerate_chunk(self, chunk: int):
        for i in self.chunks[chunk]:
            yield i, cast(T, self._data[i])

    def enumerate_chunks(self, chunks: Iterable[int]):
        for chunk in chunks:
            for i, value in self.enumerate_chunk(chunk):
                yield i, value

    def enumerate_neighborhood(self, chunk: int):
        assert 0 <= chunk and chunk < self.len
        not_left = not chunk % self.dimensions.x == 0
        not_right = not (chunk+1) % self.dimensions.x == 0
        not_top = not chunk > self.len - 2 * self.dimensions.x
        not_bottom = not chunk < self.dimensions.x

        map = (
            not_left and not_top,   not_top,  not_right and not_top,
            not_left, True, not_right,
            not_left and not_bottom, not_bottom, not_right and not_bottom
        )

        neighborhood = get_neighborhood(self.dimensions.x)
        gen = (chunk + v for b, v in zip(map, neighborhood) if b)
        return self.enumerate_chunks(gen)

    def get_neighborhood(self, position: Vector2):
        chunk = self.get_chunk_index(position)
        return self.enumerate_neighborhood(chunk)

    def get_data(self):
        return [v for v in self._data if not v is None]

    def iter_chunk(self, chunk: int):
        for _, v in self.enumerate_chunk(chunk):
            yield v

    def get_chunk(self, chunk: int):
        return [v for v in self.iter_chunk(chunk)]

    def __str__(self) -> str:
        chunk = ""
        for i, c in enumerate(self.chunks):
            chunk += f"{c}" + "\n" * \
                ((self.dimensions.x-1-i) % self.dimensions.x == 0)

        return f"{self._data}\n\n{chunk}\n{self.removed_index}"

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
