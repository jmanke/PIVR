import numpy as np
import random as rand

NUM_VECTORS = 1000

vec = []

def get_composite(vec):
    x = str(vec[0])
    y = str(vec[1])
    z = str(vec[2])

    comp_x = int(x + y + z)
    comp_y = int(y + x + z)
    comp_z = int(z + x + y)

    return (comp_x, comp_y, comp_z)


def in_range(vec, rng):
    x = vec[0]
    y = vec[1]
    z = vec[2]

    min_x = rng[0][0]
    max_x = rng[1][0]
    min_y = rng[0][1]
    max_y = rng[1][1]
    min_z = rng[0][2]
    max_z = rng[1][2]

    return min_x <= x <= max_x and min_y <= y <= max_y and min_z <= z <= max_z


for i in range(NUM_VECTORS):
    vec.append((rand.randint(0, 1000,), rand.randint(0, 1000,), rand.randint(0, 1000,)))

good = []
rng = ((100, 250, 400), (250, 500, 650))

for v in vec:
    p = in_range(v, rng)
    if p:
        print(f"In range {v}: {p}")
        good.append(v)

composites = []

comp_range = (get_composite(rng[0]), get_composite(rng[1]))

print(comp_range)

for v in vec:
    p = in_range(get_composite(v), comp_range)
    if p:
        print(f"In range {v}: {p}")
        good.append(v)


