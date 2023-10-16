
from timeit import default_timer
from Ant.Pheromone.pheromone_grid import Pheromone_Grid
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

    start_time = default_timer()
    grid = Pheromone_Grid()
    for i in range(NUMBER_OF_ITERS):
        grid.add(to_add[i])
        grid.update(TIME_STEP)
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
Number of tests: 100
Number of iters per test: 100
Median: 0.6175775000001522
Average: 0.6168156609999733
_______________________________
With numpy Cell Size 5
Number of tests: 10
Number of iters per test: 100
Median: 0.0018706000118982047
Average: 0.002016169999842532
_______________________________
With Numpy Cell Size 1
Number of tests: 10
Number of iters per test: 100
Median: 0.0021859999978914857
Average: 0.002319889992941171
"""
