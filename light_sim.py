#!/usr/bin/env python3

import cv2
import numpy as np

from scipy import interpolate

width = 1000
height = 250
num_channels = 3

# 12 ft wide, 10 used (120 in)
# 28 in high
# cable: 16 ft ea, *2 sections

num_points = 280
lightstring_original = np.array(
    [
        (100, 10),
        (10, 125),
        (100, 250),
        (250, 0),
        (375, 250),
        (400, 0),
        (550, 250),
        (750, 50),
        (1000, 175),
        (875, 250),
        (875, 125),
        (1000, 50),
        (900, 50),
        (750, 250),
        (600, 50),
        (450, 250),
        (250, 50),
        (125, 250),
    ]
)

lightstring_simple_2 = np.array(
    [
        (0, 125),
        (125, 250),
        (250, 125),
        (375, 0),
        (500, 125),
        (625, 250),
        (750, 125),
        (625, 0),
        (500, 125),
        (375, 250),
        (250, 125),
        (125, 0),
        (0, 125),
    ]
)

source_0 = 0
source_1 = 140

ctr_pts = lightstring_original
#ctr_pts = lightstring_simple_2



def interpolate_points(control_pts, num_points):
    x = control_pts[:, 0]
    y = control_pts[:, 1]
    tck, u = interpolate.splprep([x, y], k=3, s=0)
    u = np.linspace(0, 1, num=num_points, endpoint=True)
    out = interpolate.splev(u, tck)
    return out


def main():
    (lights_x, lights_y) = interpolate_points(ctr_pts, num_points)

    img = np.full((height, width, num_channels), (0, 0, 0), dtype=np.uint8)

    for i in range(num_points):
        x, y = np.intp((lights_x[i], height-lights_y[i]))
        #print(x, y)
        cv2.circle(img, (x, y), radius=4, color=(0, 0, 255), thickness=-1)


    cv2.imshow("lights", img)

    # waitKey() waits for a key press to close the window and 0 specifies indefinite loop
    cv2.waitKey(0)

    # cv2.destroyAllWindows() simply destroys all the windows we created.
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
