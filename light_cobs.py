"""
Write lights to the serial interface COBS encoded.
"""

import numpy as np

from cobs import cobs

# This project
from mycontroller import MyController


class LightCobs:
    """Represents a subset of the lights that is to be written to the serial interface
    with the COBS protocol."""

    def __init__(self, offset, num_points, port) -> None:
        self.offset = offset
        self.num_points = num_points
        self.buffer = bytearray(3 * num_points)
        self.arduino_serial = port

        gamma = 4
        self.gamma_cor = bytearray(256)
        for i in range(256):
            self.gamma_cor[i] = np.clip(int((i / 255) ** gamma * 255), 0, 255)
            # print(self.gamma_cor[i])

    def draw(self, lights, locator):
        for pixel in range(self.num_points):
            p = self.num_points - pixel - 1
            self.buffer[3 * p] = lights[self.offset + pixel][2]  # R
            self.buffer[3 * p + 1] = lights[self.offset + pixel][1]  # G
            self.buffer[3 * p + 2] = lights[self.offset + pixel][0]  # B

        if locator is not None:
            self.set_pixel(locator, color=(255, 255, 255))

        self.write_to_strip()

    def set_pixel(self, pixel, color):
        pixel -= self.offset
        if pixel < 0 or pixel >= self.num_point:
            return
        p = self.num_points - p
        self.buffer[3 * p] = color[2]  # R
        self.buffer[3 * p + 1] = color[1]  # G
        self.buffer[3 * p + 2] = color[0]  # B

    def write_to_strip(self):
        buffer = cobs.encode(self.buffer) + b"\0"
        if self.arduino_serial:
            self.arduino_serial.write(buffer)
