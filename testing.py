

from random import randint
from pygame import Vector2
from Util.chunked_data import ChunkedData


data = ChunkedData[int](Vector2(600, 600))
for _ in range(20):
    data.add(randint(0, 100), Vector2(randint(0, 599), randint(0, 599)))

print(data)
print(tuple(data.enumerate_neighbourhood(0)))
print(tuple(data.get_neighbourhood(Vector2(0, 0))))
