

import numpy as np


@np.vectorize(otypes=[np.int16, np.int16], excluded=["t"])  # type: ignore
def f(a: np.int16, b: np.int16, t: np.int16):
    return b * t, a * t


m = np.ones(9, np.int16)
n = np.zeros(9, np.int16)
print(m, n)
m, n = f(m, n, 4)
print(m, n)
