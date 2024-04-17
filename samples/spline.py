#!/usr/bin/env python3
# https://github.com/kawache/Python-B-spline-examples

import numpy as np
from scipy import interpolate

import matplotlib.pyplot as plt

# x = np.arange(0, 2*np.pi+np.pi/4, 2*np.pi/8)
# y = np.sin(x)

# ctr =np.array( [(3 , 1), (2.5, 4), (0, 1), (-2.5, 4),
##                (-3, 0), (-2.5, -4), (0, -1), (2.5, -4), (3, -1)])

num_points = 280

ctr = np.array(
    [
        (0, 0),
        (0, 125),
        (100, 250),
        (250, 0),
        (375, 250),
        (400, 0),
        (550, 250),
        (750, 50),
        (1000, 0),
        (750, 250),
        (875, 125),
        (750, 50),
        (600, 250),
        (400, 0),
        (100, 250),
        (125, 0),
        (100, 250),
    ]
)

x = ctr[:, 0]
y = ctr[:, 1]

# x=np.append(x,x[0])
# y=np.append(y,y[0])

tck, u = interpolate.splprep([x, y], k=3, s=0)
u = np.linspace(0, 1, num=num_points, endpoint=True)
out = interpolate.splev(u, tck)

plt.figure(figsize=(10, 2.5))
plt.plot(x, y, "ro", out[0], out[1], "b")
plt.legend(["Points", "Interpolated B-spline", "True"], loc="best")
plt.axis([min(x) - 1, max(x) + 1, min(y) - 1, max(y) + 1])
plt.title("B-Spline interpolation")
plt.show()
