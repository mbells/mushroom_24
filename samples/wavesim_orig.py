#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

# Parameters
num_points = 100
num_steps = 100
velocity = 0.1  # Velocity of the wave
time_step = 0.1  # Time step
damping_factor = 0.1  # Damping factor

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

# Plot the wave at the final time step
plt.plot(x, u)
plt.xlabel("Position")
plt.ylabel("Displacement")
plt.title("1D Wave Simulation")
plt.show()
