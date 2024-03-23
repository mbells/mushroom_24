#!/usr/bin/env python3
"""
The mycelium art display.

Can be drawn on an LED string or on simulated on the display.
"""

import numpy as np

import light_sim
import wavesim


# 12 ft wide, 10 used (120 in)
# 28 in high
# cable: 16 ft ea, *2 sections


num_points = 280
source_0 = 0
source_1 = num_points - 1
DAMPING_HIGH = 0.005
DAMPING_MED = 0.001
DAMPING_LOW = 0.0001

num_channels = 3

source_0 = 0
source_1 = 140

ctr_pts = light_sim.lightstring_original
crossed_points = light_sim.crossed_points_original
# ctr_pts = light_sim.lightstring_simple_2
# crossed_points = light_sim.crossed_points_simple_2

lights = np.full((num_points, num_channels), (0, 0, 0), dtype=np.uint8)


def light_waves(lights, wave0, wave1, wave2):
    boost = 0  # 100 * wave2.u
    # wave2.u *=0
    r = np.clip(0 + 150 * wave0.u + boost, 0, 255)
    g = np.clip(0 + 150 * wave1.u + boost, 0, 255)
    b = np.clip(0 + 150 * wave2.u + boost, 0, 255)
    lights[..., 0] = b
    lights[..., 1] = g
    lights[..., 2] = r


class Sparkle:
    def __init__(self, num_points):
        # self.sources =
        self.num_points = num_points
        self.sparkles = np.zeros(num_points)

    def update_lights(self, lights, wave0, wave1, wave2):
        triggers = wave0.u + wave1.u >= 1.4
        self.sparkles -= 0.2
        self.sparkles[triggers] = 1
        self.sparkles = np.clip(self.sparkles, 0, 1)
        triggers = np.where(self.sparkles)[0]
        # sparkles = self.sparkles
        # if triggers.size > 0:
        #    print("triggers", triggers)

        # self.sparkles *= 0
        for i in triggers:
            flash = np.intp(
                np.clip(i + np.random.normal(scale=3), 0, self.num_points - 1)
            )
            #print(f"{flash=}")
            lights[flash] =  np.array((255,255,255))
        

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

    lightssim = light_sim.LightsSim(ctr_pts, num_points)

    wave0 = wavesim.WaveSim(num_points, source=source_0, crossed_points=crossed_points)
    wave1 = wavesim.WaveSim(num_points, source=source_1, crossed_points=crossed_points)
    wave2 = wavesim.WaveSim(num_points, crossed_points=crossed_points)
    sparkle = Sparkle(num_points)

    locator = None

    t = 0
    while True:
        # Upadate simulation state
        t += 1

        # wave2.u = np.clip(-wave0.u - wave1.u, -1, 0)

        wave0.update_wave(t)
        wave1.update_wave(t)
        wave2.update_wave(t)
        light_waves(lights, wave0, wave1, wave2)
        sparkle.update_lights(lights, wave0, wave1, wave2)

        # Draw everything simulated
        lightssim.draw(lights, locator)

        # Respond to input
        key = lightssim.read_key()
        if key == ord("q"):
            lightssim.destroy()
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
