
import timeit


class Test:
    pass


def f(x: int):
    return ~x ^ 0


x = 100
y = 11

print(f(x), f(y))
