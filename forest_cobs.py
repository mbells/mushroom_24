# Control the LED strip for the Forest

# Written by Bernie Roehl, January 2024 for Jennifer Janik's art installation

# Read a byte from the Arduino that has one bit per touch sensor.
# Send a COBS packet to the Arduino to control the LED strip.

# Useful methods are:
#   state = read_state(current_state)    returns current_state if no data from Arduino
#   set_pixel(pixel, color)              pixel is an index, color is (r, g, b)
#   write_to_strip()                     sends the color array to the strip

import cv2
import numpy as np
import serial
import time

from cobs import cobs

# This project
import myconfig
from mycontroller import MyController
from light_cobs import LightCobs

### Arduino interface ###


arduino_serial_1 = None
#arduino_serial_1 = serial.Serial("COM4", 115200)
arduino_serial_2 = None
#arduino_serial_2 = serial.Serial("COM5", 115200)

width = 1000
height = 250
num_channels = 3



def read_state(inputs):
    while arduino_serial_1 and arduino_serial_1.in_waiting:
        state = arduino_serial_1.read()[0]
        inputs = [state & 1 != 0, state & 2 != 0]
    return inputs


class Lights(MyController):
    def __init__(self, num_points):
        self.num_points = num_points
        self.inputs = [False, False]
        self.lights_1 = LightCobs(0, 140, arduino_serial_1)
        self.lights_2 = LightCobs(140, 140, arduino_serial_2)
        self.img = np.full((height, width, num_channels), (0, 0, 0), dtype=np.uint8)

    def destroy(self):
        pass

    def draw(self, lights, locator):
        self.lights_1.draw(lights, locator)
        self.lights_2.draw(lights, locator)

        # Fake image required so that input is processed
        cv2.imshow("lights", self.img)

    def get_inputs(self):
        self.inputs = read_state(self.inputs)
        return self.inputs


    def read_key(self):
        key = cv2.waitKey(1)

        if key == ord("1"):
            self.inputs[0] = not self.inputs[0]
            key = -1
        elif key == ord("2"):
            self.inputs[1] = not self.inputs[1]
            key = -1

        return key


### Keep track of when the state last changed ###

changed_times = 8 * [
    0
]  # time at which each sensor was touched (maximum of 8 sensors, i.e. one byte from Arduino)


def update_changed_times(state, previous_state):
    changed = state ^ previous_state
    for which_sensor in range(8):
        if changed & state & (1 << which_sensor):
            changed_times[which_sensor] = time.time()

### Effects ###

NUM_PIXELS = myconfig.NUM_POINTS
lights = LightCobs(0, NUM_PIXELS, "COM5")


SPREAD = (
    5  # how many pixels in each direction (forward and back) the pixel arm spreads out
)
SPREAD_TIME = 3  # how long it takes to spread out

sensor_map = [  # indexed by sensor, each entry is array of pixel indices
    [15, 52, 100],
    [100, 120, 95],
]

sensor_colors = [(255, 0, 0), (0, 255, 0)]  # indexed by sensor, gives color


def draw_arm(pt, color, fraction):
    color = (
        int(fraction * color[0]),
        int(fraction * color[1]),
        int(fraction * color[2]),
    )
    lights.set_pixel(pt, color)
    for offset in range(1, SPREAD):
        c = (color[0] >> offset, color[1] >> offset, color[2] >> offset)
        lights.set_pixel(pt - offset, c)
        lights.set_pixel(pt + offset, c)



def update_LEDs(state):
    for i in range(NUM_PIXELS):
        lights.set_pixel(i, (0, 0, 0))  # clear array
    for sensor in range(len(sensor_map)):
        if changed_times[sensor] == 0:
            continue
        fraction = (time.time() - changed_times[sensor]) / SPREAD_TIME
        if fraction > 1:
            fraction = 1
        if (state & (1 << sensor)) == 0:
            fraction = 1 - fraction  # if bit is off, reverse fade direction
        color = sensor_colors[sensor]
        for pt in sensor_map[sensor]:
            draw_arm(pt, color, fraction)


### Main loop ###


def main():
    state = previous_state = 0
    while True:
        previous_state = state
        state = read_state(state)
        print(state)
        update_changed_times(state, previous_state)
        update_LEDs(state)
        lights.write_to_strip()


if __name__ == "__main__":
    main()
