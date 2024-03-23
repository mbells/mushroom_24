#!/usr/bin/env python3
"""
Simulate a string of LEDs on the screen.

Meant to be called from mycelium.
"""

import cv2
import numpy as np

from scipy import interpolate


width = 1000
height = 250
num_channels = 3
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
crossed_points_original = [(119, 214)]

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
crossed_points_simple_2 = [(70, 210)]


class LightsSim:
    def __init__(self, ctr_pts, num_points):
        (self.lights_x, self.lights_y) = self.interpolate_points(ctr_pts, num_points)

        self.img = np.full((height, width, num_channels), (0, 0, 0), dtype=np.uint8)

    def destroy(self):
        cv2.destroyAllWindows()

    def draw(self, lights, locator):
        self.img *= 0

        for i in range(num_points):
            x, y = np.intp((self.lights_x[i], height - self.lights_y[i]))
            c = lights[i].tolist()
            cv2.circle(self.img, (x, y), radius=4, color=c, thickness=-1)

        if locator is not None:
            x, y = np.intp((self.lights_x[locator], height - self.lights_y[locator]))
            # print(x,y)
            cv2.circle(iself.mg, (x, y), radius=6, color=(255, 255, 255), thickness=2)

        cv2.imshow("lights", self.img)

    def interpolate_points(self, control_pts, num_points):
        x = control_pts[:, 0]
        y = control_pts[:, 1]
        tck, u = interpolate.splprep([x, y], k=3, s=0)
        u = np.linspace(0, 1, num=num_points, endpoint=True)
        out = interpolate.splev(u, tck)
        return out

    def read_key(self):
        return cv2.waitKey(1)


# -------------- old


ctr_pts = lightstring_original
# crossed_points = crossed_points_original
# ctr_pts = lightstring_simple_2
# crossed_points = crossed_points_simple_2


def move_locator(locator, amount):
    if locator is None:
        return None
    locator += amount
    if locator < 0:
        locator += num_points
    if locator >= num_points:
        locator -= num_points
    print(locator)
    return locator


def main():

    lightssim = LightsSim(ctr_pts, num_points)

    lights = np.full((num_points, num_channels), (100, 100, 100), dtype=np.uint8)
    locator = None

    t = 0
    while True:
        # Upadate simulation state
        t += 1

        # wave2.u = np.clip(-wave0.u - wave1.u, -1, 0)

        # Draw everything simulated
        lightssim.draw(lights, locator)

        # Respond to input
        key = cv2.waitKey(1)
        if key == ord("q"):
            cv2.destroyAllWindows()
            break
        elif key == ord("l"):
            print("locator")
            if locator is None:
                locator = 0
            else:
                locator = None
        elif key == -1:
            pass
        elif key == 151 or key == 82:  # Up
            locator = move_locator(locator, 1)
        elif key == 154 or key == 85:  # PgUp
            locator = move_locator(locator, 10)
        elif key == 153 or key == 84:  # Down
            locator = move_locator(locator, -1)
        elif key == 155 or key == 86:  # PageDown
            locator = move_locator(locator, -10)
        else:
            print(f"Unknown key {key}")


if __name__ == "__main__":
    main()
