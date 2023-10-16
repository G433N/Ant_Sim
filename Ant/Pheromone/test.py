from typing import Any
import numpy as np


radius = 20
prec_exp = 7
# | 6: 64 | 8: 256 | 10: 1024 | (reminder on how binary works)

precision = 2**prec_exp
quarter_prec = 2**(prec_exp-2)

quarter_angle_arr = np.empty((quarter_prec, radius, 2), dtype=np.int8)


y_from_angle_indexes = (
    np.cos((np.pi/2) * (i / quarter_prec))
    for i in range(quarter_prec)
)

arccos_chsh_arr = (
    np.fromiter(
        y_from_angle_indexes,
        dtype=float,
        count=quarter_prec
    )
)
print(arccos_chsh_arr)

def find_closest_angle_index(dir: np.ndarray[float,np.dtype[Any]]):
    index_offset = 0
    match np.sign(dir[0]),np.sign(dir[1]):
        case    1   ,   1|0    :
            x = dir[0]
        case    -1|0,   1      :
            x = dir[1]
            index_offset = quarter_angle_arr
        case    -1  ,   -1|0   :
            x = -dir[0]
            index_offset = 2 * quarter_angle_arr
        case    1|0 ,   -1     :
            x = -dir[1]
            index_offset = 3 * quarter_angle_arr
        case _:
            raise ValueError("How did u find this angle???")
    
    bin_search_step = (1<<(prec_exp-3))
    index = bin_search_step-1
    for _ in range(prec_exp-3):
        bin_search_step >>= 1
        if x <= arccos_chsh_arr[index]:
            index += bin_search_step
        else:
            index -= bin_search_step
        
    return index + index_offset




for r in range(radius):
    for i in range(quarter_prec):
        angle = (np.pi/2) * (i / quarter_prec)
        x = round((r+1)*np.cos(angle))
        y = round((r+1)*np.sin(angle))
        quarter_angle_arr[i, r] = (x, y)

angle_sorted_arr = np.empty((precision, radius, 2), dtype=np.int8)

for r in range(radius):
    for i in range(quarter_prec):
        x, y = quarter_angle_arr[i, r]
        angle_sorted_arr[i, r] = (x, y)
        angle_sorted_arr[quarter_prec+i, r] = (-y, x)
        angle_sorted_arr[2*quarter_prec+i, r] = (-x, -y)
        angle_sorted_arr[3*quarter_prec+i, r] = (y, -x)
