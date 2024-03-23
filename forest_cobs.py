# Control the LED strip for the Forest

# Written by Bernie Roehl, January 2024 for Jennifer Janik's art installation

# Read a byte from the Arduino that has one bit per touch sensor.
# Send a COBS packet to the Arduino to control the LED strip.

# Useful methods are:
#   state = read_state(current_state)    returns current_state if no data from Arduino
#   set_pixel(pixel, color)              pixel is an index, color is (r, g, b)
#   write_to_strip()                     sends the color array to the strip

import serial
import sys
import time

from cobs import cobs
from msvcrt import kbhit

# This project
from mycontroller import MyController

### LED strip buffer ###

NUM_PIXELS = 140

buffer = bytearray(3 * NUM_PIXELS)


def set_pixel(pixel, color):
    if pixel < 0 or pixel >= NUM_PIXELS:
        return
    buffer[3 * pixel] = color[0]  # B
    buffer[3 * pixel + 1] = color[1]  # R
    buffer[3 * pixel + 2] = color[2]  # G


### Arduino interface ###

arduino_serial = serial.Serial("COM5" if len(sys.argv) < 2 else sys.argv[1], 115200)


def read_state(state):
    while arduino_serial and arduino_serial.in_waiting:
        state = arduino_serial.read()[0]
    return state


def write_to_strip():
    if arduino_serial:
        arduino_serial.write(cobs.encode(buffer) + b"\0")
    time.sleep(0.03)


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
    set_pixel(pt, color)
    for offset in range(1, SPREAD):
        c = (color[0] >> offset, color[1] >> offset, color[2] >> offset)
        set_pixel(pt - offset, c)
        set_pixel(pt + offset, c)


def update_LEDs(state):
    for i in range(NUM_PIXELS):
        set_pixel(i, (0, 0, 0))  # clear array
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


class Lights(MyController):
    def __init__(self, num_points):
        self.num_points = num_points
        self.state = 0

    def destroy(self):
        pass

    def draw(self, lights, locator):
        for pixel in range(self.num_points):
            buffer[3 * pixel] = lights[pixel][0]  # B
            buffer[3 * pixel + 1] = lights[pixel][2]  # R
            buffer[3 * pixel + 2] = lights[pixel][1]  # G

        if locator is not None:
            set_pixel(locator, color=(255, 255, 255))

        write_to_strip()

    def get_inputs(self):
        self.state = read_state(self.state)
        return (self.state & 1 != 0, self.state & 2 != 0)


    def read_key(self):
        key = -1
        is_key_pressed = not kbhit()
        if is_key_pressed:
            key = 'q'
        
        return key

### Main loop ###


def main():
    state = previous_state = 0
    while True:
        previous_state = state
        state = read_state(state)
        print(state)
        update_changed_times(state, previous_state)
        update_LEDs(state)
        write_to_strip()


if __name__ == "__main__":
    main()
