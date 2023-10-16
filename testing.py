import numpy as np


a = np.ones((3, 2))
b = np.expand_dims(np.sum(a, axis=1), axis=1)
print(b)
print(np.tile(b, (1, 2)))
