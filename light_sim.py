#!/usr/bin/env python3

import cv2
import numpy as np

from scipy import interpolate

import wavesim

width = 1000
height = 250
num_channels = 3

# 12 ft wide, 10 used (120 in)
# 28 in high
# cable: 16 ft ea, *2 sections


num_points = 280
source_0 = 0
source_1 = num_points - 1
DAMPING_HIGH = 0.005
DAMPING_MED = 0.001
DAMPING_LOW = 0.0001

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

source_0 = 0
source_1 = 140

ctr_pts = lightstring_original
crossed_points = crossed_points_original
# ctr_pts = lightstring_simple_2
# crossed_points = crossed_points_simple_2

lights = np.full((num_points, num_channels), (0, 0, 0), dtype=np.uint8)


def light_waves(lights, wave0, wave1, wave2):
    r = np.clip(100 + 200 * wave0.u, 0, 255)
    g = np.clip(100 + 200 * wave1.u, 0, 255)
    b = np.clip(100 + 200 * wave2.u, 0, 255)
    lights[..., 0] = b
    lights[..., 1] = g
    lights[..., 2] = r


class LightsSim:
    def __init__(self, ctr_pts, num_points):
        (self.lights_x, self.lights_y) = self.interpolate_points(ctr_pts, num_points)

    def interpolate_points(self, control_pts, num_points):
        x = control_pts[:, 0]
        y = control_pts[:, 1]
        tck, u = interpolate.splprep([x, y], k=3, s=0)
        u = np.linspace(0, 1, num=num_points, endpoint=True)
        out = interpolate.splev(u, tck)
        return out

    def draw(self, img, lights):
        for i in range(num_points):
            x, y = np.intp((self.lights_x[i], height - self.lights_y[i]))
            c = lights[i].tolist()
            cv2.circle(img, (x, y), radius=4, color=c, thickness=-1)


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

    wave0 = wavesim.WaveSim(num_points, source=source_0, crossed_points=crossed_points)
    wave1 = wavesim.WaveSim(num_points, source=source_1, crossed_points=crossed_points)
    wave2 = wavesim.WaveSim(num_points, crossed_points=crossed_points)

    img = np.full((height, width, num_channels), (0, 0, 0), dtype=np.uint8)
    locator = None

    t = 0
    while True:
        t += 1
        wave0.update_wave(t)
        wave1.update_wave(t)
        wave2.update_wave(t)
        light_waves(lights, wave0, wave1, wave2)
        img *= 0
        lightssim.draw(img, lights)

        if locator is not None:
            x, y = np.intp(
                (lightssim.lights_x[locator], height - lightssim.lights_y[locator])
            )
            # print(x,y)
            cv2.circle(img, (x, y), radius=6, color=(255, 255, 255), thickness=2)

        cv2.imshow("lights", img)

        key = cv2.waitKey(1)
        if key == ord("q"):
            cv2.destroyAllWindows()
            break
        elif key == ord("1"):
            wave0.source_active = not wave0.source_active
        elif key == ord("2"):
            wave1.source_active = not wave1.source_active
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

        # Adjust simulation parameters...
        if wave0.source_active and wave1.source_active:
            wave0.damping_factor = DAMPING_LOW
            wave1.damping_factor = DAMPING_LOW
        elif wave0.source_active or wave1.source_active:
            wave0.damping_factor = DAMPING_MED
            wave1.damping_factor = DAMPING_MED
        else:
            wave0.damping_factor = DAMPING_HIGH
            wave1.damping_factor = DAMPING_HIGH


if __name__ == "__main__":
    main()
