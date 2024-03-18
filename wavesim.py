#!/usr/bin/env python3

import numpy as np
import cv2

# Parameters
num_points = 100
num_steps = 100
velocity = 0.1  # Velocity of the wave
time_step = 0.1  # Time step
damping_factor = 0.1  # Damping factor

width = 1000
height = 250
num_channels = 3


# Initial conditions
x = np.arange(num_points)
u = np.zeros(num_points)  # Initial displacement
u[int(num_points / 2)] = 1.0  # Initial impulse

# Simulation
for step in range(num_steps):
    # Update displacement using wave equation
    u[1:-1] += velocity**2 * time_step**2 * (u[:-2] - 2 * u[1:-1] + u[2:])
    # Apply damping
    u *= 1 - damping_factor * time_step
    # Boundary conditions (fixed ends)
    u[0] = 0
    u[-1] = 0


img = np.full((height, width, num_channels), (0, 0, 0), dtype=np.uint8)

# Plot the wave at the final time step
plt.plot(x, u)
plt.xlabel("Position")
plt.ylabel("Displacement")
plt.title("1D Wave Simulation")
plt.show()

cv2.imshow("lights", img)

# waitKey() waits for a key press to close the window and 0 specifies indefinite loop
cv2.waitKey(0)

# cv2.destroyAllWindows() simply destroys all the windows we created.
cv2.destroyAllWindows()
