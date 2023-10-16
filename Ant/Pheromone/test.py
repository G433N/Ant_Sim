radius = 10
precision = 10
dict_of_points: list[list[tuple[int,int]]] = [[] for _ in range(precision+1)]
for x in range(radius+1):
    for y in range(x+1):
        if x:
            dict_of_points[precision*y//x].append((x,y))

l = 8
s = 1

print([dict_of_points[i+s][:] for i in range(l)])

