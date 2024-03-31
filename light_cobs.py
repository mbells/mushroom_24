"""
Write lights to the serial interface COBS encoded.
"""

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


    def draw(self, lights, locator):
        for pixel in range(self.num_points):
            self.buffer[3 * pixel] = lights[self.offset+pixel][0]  # B
            self.buffer[3 * pixel + 1] = lights[self.offset+pixel][2]  # R
            self.buffer[3 * pixel + 2] = lights[self.offset+pixel][1]  # G

        if locator is not None:
            self.set_pixel(locator, color=(255, 255, 255))

        self.write_to_strip()


    def set_pixel(self, pixel, color):
        pixel -= self.offset
        if pixel < 0 or pixel >= self.num_point:
            return
        self.buffer[3 * pixel] = color[0]  # B
        self.buffer[3 * pixel + 1] = color[1]  # R
        self.buffer[3 * pixel + 2] = color[2]  # G

    def write_to_strip(self):
        buffer = cobs.encode(self.buffer) + b"\0"
        if self.arduino_serial:
            self.arduino_serial.write(buffer)
