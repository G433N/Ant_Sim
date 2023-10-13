

from timeit import default_timer

from pygame import Vector2
from Ant.Food.food import Food
from Ant.simple_ants import SimpleAnts
from Util.globals import WORLD_SIZE
from Util.util import random_vector


NUMBER_OF_TESTS = 10
NUMBER_OF_ITERS = 1000
TIME_STEP = 1/60


result: list[float] = list()


def get_to_add_list():
    return [
        random_vector(WORLD_SIZE) for _ in range(NUMBER_OF_ITERS)
    ]


print("DO NOT RUN IN DEBUG")
for test in range(NUMBER_OF_TESTS):

    to_add = get_to_add_list()
    food = Food()
    food.add(WORLD_SIZE/4, 20, 100)
    food.add(Vector2(100, 500), 20, 100)
    food.add(WORLD_SIZE/4 + Vector2(700, 0), 20, 100)
    food.add(3 * WORLD_SIZE/4, 20, 100)

    start_time = default_timer()
    ants = SimpleAnts(lambda position: None)
    ants.food = food
    for i in range(NUMBER_OF_ITERS):
        ants.add(to_add[i])
        ants.update(TIME_STEP)

    end_time = default_timer() - start_time
    print(test, end_time)
    result.append(end_time)

median = result[NUMBER_OF_TESTS // 2]
average = sum(result) / NUMBER_OF_TESTS

print(f"Number of tests: {NUMBER_OF_TESTS}")
print(f"Number of iters per test: {NUMBER_OF_ITERS}")
print(f"Median: {median}")
print(f"Average: {average}")

"""
Number of tests: 10
Number of iters per test: 1000
Median: 6.349868299999798
Average: 6.1996555199997605
______________________________
If classes instead of lists
Number of tests: 10
Number of iters per test: 1000
Median: 5.732934099999511
Average: 5.741801739999846
"""
