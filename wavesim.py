#!/usr/bin/env python3

import numpy as np
import cv2

# Parameters
num_points = 280
num_steps = 1000
velocity = 0.1  # Velocity of the wave
time_step = 1  # Time step
x_step = 1
damping_factor = 0.001  # Damping factor

width = 1000
height = 250
num_channels = 3


# Initial conditions
x = np.arange(num_points)
u = np.zeros(num_points)  # Initial displacement
u_1 = np.zeros(num_points)  # Last step (u[t-1])
u_next = np.zeros(num_points)  # Next step, used temporarily


u[int(num_points / 2)] = 1.0  # Initial impulse

rsq=(velocity*time_step/x_step)**2

"""
# Simulation
for step in range(num_steps):
    # Update displacement using wave equation
    u[1:-1] += velocity**2 * time_step**2 * (u[:-2] - 2 * u[1:-1] + u[2:])
    # Apply damping
    u *= 1 - damping_factor * time_step
    # Boundary conditions (fixed ends)
    u[0] = 0
    u[-1] = 0
"""

def update_wave():
    # Update displacement using wave equation
    #u[1:-1] += rsq * (u[:-2] - 2 * u[1:-1] + u[2:])

    global u, u_1, u_next

    for a in range(1, len(u)-1):
        u_next[a] = 2*(1-rsq)*u[a]-u_1[a]+rsq*(u[a-1]+u[a+1])
        # Rotate; `next` will be overwritten but this avoids memory allocation

    u, u_1, u_next = u_next, u, u_1
    np.clip(u, -1, 1, out=u)
    
    # Apply damping
    u *= 1 - damping_factor * time_step
    # Boundary conditions (fixed ends)
    u[0] = 0
    u[-1] = 0

def update_wave_vec(u):
    """Vectorized version of update.
    Doesn't work yet...
    """
    rsq = velocity**2 * time_step**2
    # Update displacement using wave equation
    u[1:-1] += rsq * (u[:-2] - 2 * u[1:-1] + u[2:])


    # Refactoring   
    tmp = u
    u += 2*(1-rsq)*u[a] - u1[a] + rsq*(u[a-1]+u[a+1])

    u += 2*u[a] - 2*rsq*u[a] + rsq*(u[a-1]+u[a+1])  - u1[a]

    u1 = tmp
    #u1, u = u, tmp



    # Apply damping
    u *= 1 - damping_factor * time_step
    # Boundary conditions (fixed ends)
    u[0] = 0
    u[-1] = 0


def draw(img, u):
    img *= 0
    for i in range(num_points):
        x, y = np.intp((4*i, 100*u[i]))
        #print("x,y=", x, y)
        cv2.circle(img, (x, y), radius=4, color=(0, 0, 255), thickness=-1)


img = np.full((height, width, num_channels), (0, 0, 0), dtype=np.uint8)
for step in range(num_steps):
    #print(f"===== {step}")
    #if step == 1:
    #    print(u)
    update_wave()
    draw(img, u)
    cv2.imshow("lights", img)
    if cv2.waitKey(1) == ord('q'):
        cv2.destroyAllWindows()
        break