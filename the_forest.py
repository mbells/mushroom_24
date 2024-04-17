# Control the LED strip for the Forest

# Written by Bernie Roehl, January 2024 for Jennifer Janik's art installation

# Read a byte from the Arduino that has one bit per touch sensor.
# Send a COBS packet to the Arduino to control the LED strip.

# Useful methods are:
#   state = read_state(current_state)    returns current_state if no data from Arduino
#   set_pixel(pixel, color)              pixel is an index, color is (r, g, b)
#   write_to_strip()                     sends the color array to the strip

import sys, time, random
import serial
from cobs import cobs
from msvcrt import kbhit, getch

### LED strip buffer ###

NUM_PIXELS = 100

buffer = bytearray(3 * NUM_PIXELS)

def set_pixel(pixel, color):
	if pixel < 0 or pixel >= NUM_PIXELS: return
	buffer[3*pixel] = color[0]
	buffer[3*pixel+1] = color[1]
	buffer[3*pixel+2] = color[2]

arduino_serial1 = serial.Serial("COM4" if len(sys.argv) < 2 else sys.argv[1], 115200)

def read_state(state):
	while arduino_serial1 and arduino_serial1.in_waiting: state = arduino_serial1.read()[0]
	return state

def write_to_strip():
	if arduino_serial1: arduino_serial1.write(cobs.encode(buffer) + b'\0')
	time.sleep(0.1)

def update_LEDs(state):
	if state == 0:
		for i in range(NUM_PIXELS): set_pixel(i, (20,20,20))
	elif state == 1:
		for i in range(NUM_PIXELS): set_pixel(i, (int(255.0 * i / NUM_PIXELS), 0, 0))
	elif state == 2:
		for i in range(NUM_PIXELS): set_pixel(NUM_PIXELS - i - 1, (0, int(255.0 * i / NUM_PIXELS), 0))
	elif state == 3:
		for i in range(NUM_PIXELS): set_pixel(i, (random.randint(0,255),random.randint(0,255),random.randint(0,255)))

def main():
	state = 0
	while True:
		if kbhit():  # debugging '1' and '2' toggle touches
			c = ord(getch())
			if c == 27: sys.exit(0)
			if c == 49: state ^= 1
			if c == 50: state ^= 2
		state = read_state(state)
		print(f"{state}\r", end="")
		update_LEDs(state)
		write_to_strip()

if __name__ == "__main__": main()

