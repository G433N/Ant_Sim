
from dataclasses import dataclass
import random
import timeit


@dataclass(slots=True)
class Test:
    test: int
    x: float


n = 10000
start_time = timeit.default_timer()
a = list(i for i in range(n))
random.shuffle(a)
print(a)
print("Shuffle list", timeit.default_timer() - start_time)


start_time = timeit.default_timer()
t = list(Test(random.randint(0, 1000), random.random()) for _ in range(n))
print("Test list", timeit.default_timer() - start_time)
d: dict[int, Test] = dict()


start_time = timeit.default_timer()
for x, y in zip(a, t):
    d[x] = y
print("fill dict", timeit.default_timer() - start_time)

start_time = timeit.default_timer()
while len(d):
    d.popitem()
print("empty dict", timeit.default_timer() - start_time)
