#!/usr/bin/env python3
"""
The mycelium art display.

Outputs simulation to display and optionally write to serial.

Keys:
- q - quit
- 1, 2 - toggle inputs
- l - locator
- Up, Dn, PgUp, PgDown - move locator
"""

import argparse
import numpy as np

# This project
import forest_cobs
import light_sim
import myconfig
import wavesim
from mycontroller import MyController, MyModel


# 12 ft wide, 10 used (120 in)
# 28 in high
# cable: 16 ft ea, *2 sections

DAMPING_HIGH = 0.005
DAMPING_MED = 0.001
DAMPING_LOW = 0.0001

num_channels = 3

# ctr_pts = light_sim.lightstring_original
# ctr_pts = light_sim.lightstring_simple_2
ctr_pts = light_sim.lightstring_simple_final
crossed_points = light_sim.crossed_points_simple_final


def args_parser():
    parser = argparse.ArgumentParser(
        # prog='mycelium',
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="See https://github.com/mbells/mushroom_24",
    )

    parser.add_argument("target", type=str, choices=["one", "two"])

    parser.add_argument("--cobs", action="store_true")
    parser.add_argument("--test", type=str)

    # parser.add_argument('--two', action='store_true')
    return parser.parse_args()


def light_waves(lights, wave0, wave1, wave2):
    background = 50 * wave2.u
    # wave2.u *=0
    r = np.clip(0 + 150 * wave0.u + background, 0, 255)
    g = np.clip(0 + 150 * wave1.u + background, 0, 255)
    b = np.clip(0 + 150 * wave2.u + background, 0, 255)
    lights[..., 0] = b
    lights[..., 1] = g
    lights[..., 2] = r


class Sparkle:
    def __init__(self, num_points):
        # self.sources =
        self.num_points = num_points
        self.sparkles = np.zeros(num_points)

    def update_lights(self, lights, wave0, wave1, wave2):
        # Fade existing ones
        self.sparkles -= 0.1
        # Add new ones
        triggers = wave0.u + wave1.u >= 1.4
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
            # print(f"{flash=}")
            intensity = self.sparkles[i]
            lights[flash] = np.array((255, 255, 255)) - (1 - intensity)


def test_pattern(pattern, lights):
    if pattern == "white":
        lights[..., 0] = 255
        lights[..., 1] = 255
        lights[..., 2] = 255
    if pattern == "red":
        lights[..., 0] = 0
        lights[..., 1] = 0
        lights[..., 2] = 255
    if pattern == "green":
        lights[..., 0] = 0
        lights[..., 1] = 255
        lights[..., 2] = 0
    if pattern == "blue":
        lights[..., 0] = 255
        lights[..., 1] = 0
        lights[..., 2] = 0


def move_locator(locator, amount):
    if locator is None:
        return None
    locator += amount
    if locator < 0:
        locator += myconfig.NUM_POINTS
    if locator >= myconfig.NUM_POINTS:
        locator -= myconfig.NUM_POINTS
    print(locator)
    return locator


def main():
    args = args_parser()

    if args.target == "one":
        myconfig.NUM_POINTS = 100
        crossed_points = myconfig.crossed_points_1
    elif args.target == "two":
        myconfig.NUM_POINTS = 280
        crossed_points = myconfig.crossed_points_2

    source_0 = myconfig.source_0
    source_1 = myconfig.source_1

    # crossed_points = []

    lights = np.full((myconfig.NUM_POINTS, num_channels), (0, 0, 0), dtype=np.uint8)
    model = MyModel()
    controller = light_sim.LightsSim(model, ctr_pts, myconfig.NUM_POINTS)

    if args.cobs:
        cobs = forest_cobs.Lights(model, myconfig.NUM_POINTS)
    else:
        cobs = MyController(model)

    wave0 = wavesim.WaveSim(
        myconfig.NUM_POINTS, source=source_0, crossed_points=crossed_points
    )
    wave1 = wavesim.WaveSim(
        myconfig.NUM_POINTS, source=source_1, crossed_points=crossed_points
    )
    wave2 = wavesim.WaveSim(myconfig.NUM_POINTS, crossed_points=crossed_points)
    sparkle = Sparkle(myconfig.NUM_POINTS)

    # Background wave
    wave2.damping_factor = 0
    wave2.set_velocity(0.2)

    locator = None

    print(__doc__)

    t = 0
    while True:

        # Every so often, reset the simulation of wave2 (background)
        if t == 5000:
            print("Resetting background wave")
            t = 0
        if t == 0:
            wave2.u *= 0
            wave2.u[1] = wave2.u[2] = wave2.u[3] = wave2.u[myconfig.NUM_POINTS - 2] = (
                wave2.u[myconfig.NUM_POINTS - 3]
            ) = wave2.u[myconfig.NUM_POINTS - 4] = 3

        # Upadate simulation state
        t += 1

        # wave2.u = np.clip(-wave0.u - wave1.u, -1, 0)

        wave0.update_wave(t)
        wave1.update_wave(t)
        wave2.update_wave(t)
        light_waves(lights, wave0, wave1, wave2)
        sparkle.update_lights(lights, wave0, wave1, wave2)

        test_pattern(args.test, lights)

        # Draw everything simulated
        controller.draw(lights, locator)
        cobs.draw(lights, locator)

        # Respond to input
        key = controller.read_key()
        if key == ord("q"):
            controller.destroy()
            break
        elif key == ord("l"):
            print("locator")
            if locator is None:
                locator = 0
            else:
                locator = None
        elif key == -1:
            pass
        elif key in {151, 82, 2490368}:  # Up
            locator = move_locator(locator, 1)
        elif key in {154, 85, 2162688}:  # PgUp
            locator = move_locator(locator, 10)
        elif key in {153, 84, 2621440}:  # Down
            locator = move_locator(locator, -1)
        elif key in {155, 86, 2228224}:  # PageDown
            locator = move_locator(locator, -10)
        else:
            print(f"Unknown key {key}")

        cobs.process_inputs()
        if (
            wave0.source_active != model.sensors[0]
            or wave1.source_active != model.sensors[1]
        ):
            print("input", model.sensors[0], model.sensors[1])
            wave0.source_active = model.sensors[0]
            wave1.source_active = model.sensors[1]

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
