import numpy as np

for n in range(3, 100):
    tri = n - 2
    maxVerts = np.floor(2 * n / 3) + 2
    # poly1 = np.floor(2 * n / 3)
    # poly2 = np.floor(n / 3) - 1
    # total = poly1 + poly2 + 4
    # good = True
    # if total - n > 2:
    #     good = False
    # print("n = ", n, ", maxVerts = ", maxVerts, ", poly1 = ", poly1 + 2, ", poly2 = ", poly2 + 2, ", total = ", total, ", Good = ", good)

    low_bound = np.floor(n / 3) + 1
    remaining = n + 2 - low_bound
    good = True
    if remaining > maxVerts:
        good = False

    print("n = ", n, ", maxVerts = ", maxVerts, ", low bound = ", low_bound, ", remaining = ", remaining, ", good = ", good)