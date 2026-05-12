# find_intersection.py from stack overflow
# "How to find the intersection points between two plotted curves in matplotlib?
# TMM: didn't work out of the box. edited to switch curves and invert
# intersection y

import numpy as np
from matplotlib import pyplot as plt
from copy import deepcopy


def find_intersection(t, curve1_, curve2_):
    if curve1_[0]<curve2_[0]:
        curve1=deepcopy(curve2_)
        curve2=deepcopy(curve1_)
    else:
        curve1=deepcopy(curve1_)
        curve2=deepcopy(curve2_)
    intersection = []
    prev_dif = 0
    t0, prev_c1, prev_c2 = 0, None, None
    for t1, c1, c2 in zip (t, curve1, curve2):
        new_dif = c1-c2
        print(f"new_dif = {new_dif}")
        if np.abs(new_dif) < 1e-12:
            intersection.append((t1, c1))
        elif new_dif < 0:
            denom = prev_dif - new_dif
            intersection.append(((-new_dif*t0 + prev_dif*t1) / denom, -(c1*prev_c2 - c2*prev_c1)/ denom))
            break
        t0, prev_c1, prev_c2, prev_dif = t1, c1, c2, new_dif
    return intersection

if __name__=="__main__":
    plt.ion()
    N=12
    t=np.linspace(0,50, N)
    curve1 = np.sin(t*.08 +1.4)*np.random.uniform(0.5, 0.9) + 1
    curve2 = -np.cos(t*0.07+.1)*np.random.uniform(0.7, 1.0) + 1
    fig, ax = plt.subplots()
    ax.plot(t, curve1, 'b-')
    ax.plot(t, curve1, 'bo')
    ax.plot(t, curve2, 'r-')
    ax.plot(t, curve2, 'ro')
    intersection = find_intersection(t, curve1, curve2)
    print(intersection)
    ax.plot(*zip(*intersection), 'go', alpha=0.7, ms=10)
    plt.show()
