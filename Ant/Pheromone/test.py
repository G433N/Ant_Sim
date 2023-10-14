


from typing import Any
import numpy
np = numpy
shape = (3,5)
x = 3
m: np.ndarray[int, np.dtype[Any]] = np.zeros(shape,int)


m[2][1] += 8
m[1][3] += 43




def diffusion(arr: np.ndarray[int, np.dtype[Any]]):
    vertical_arr = diffusion_stack(arr)
    horizon_arr = diffusion_stack(np.transpose(arr))
    return (
        vertical_arr[:-2]
        + vertical_arr[2:]
        + np.transpose(
            horizon_arr[:-2]
            + horizon_arr[2:]
        )
        - 4*arr
    )


def diffusion_stack(arr: np.ndarray[int, np.dtype[Any]]):
    return np.vstack((arr[0], arr, arr[-1]))

def diffused_array(arr: np.ndarray[int, np.dtype[Any]]):
    return arr + diffusion(arr//6)


print(f"{m}\n")
for i in range(2):
    m = diffused_array(m)
    print(f"{m}\n")