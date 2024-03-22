#!/usr/bin/env python3

import numpy as np
import cv2
import math

# Parameters
num_points = 280
velocity = 0.1  # Velocity of the wave
time_step = 1  # Time step
x_step = 1
cfg_damping_factor = 0.0001  # Damping factor
source_freq = 1 / 100

width = 1000
height = 250
num_channels = 3

crossed_points = []
#crossed_points = [(40, 100)]
#crossed_points = [(119, 214)]

# source_0 = int(num_points / 2)
source_0 = 0


class WaveSim:
    def __init__(self, num_points, source=None, crossed_points=[]):
        self.num_points = num_points
        self.source = source
        self.crossed_points = crossed_points

        # Initial conditions
        self.x = np.arange(num_points)
        self.u = np.zeros(num_points)  # Initial displacement
        self.u_1 = np.zeros(num_points)  # Last step (u[t-1])
        self.u_next = np.zeros(num_points)  # Next step, used temporarily

        self.rsq = (velocity * time_step / x_step) ** 2
        self.source_active = False
        self.damping_factor = cfg_damping_factor

    def update_wave(self, step):
        # Update displacement using wave equation
        # u[1:-1] += rsq * (u[:-2] - 2 * u[1:-1] + u[2:])

        # global u, u_1, u_next, source_freq
        u = self.u
        u_next = self.u_next
        u_1 = self.u_1
        rsq = self.rsq

        for a in range(1, len(u) - 1):
            u_next[a] = 2 * (1 - rsq) * u[a] - u_1[a] + rsq * (u[a - 1] + u[a + 1])

        np.clip(u_next, -1, 1, out=u_next)

        # Apply damping
        u_next *= 1 - self.damping_factor * time_step
        # Boundary conditions (fixed ends)
        u_next[0] = 0
        u_next[-1] = 0

        # When crosses are defined, these affect each other:
        for a, b in self.crossed_points:
            avg = np.mean([u_next[a], u_next[b]])
            u_next[a] = u_next[b] = avg

        # if np.isclose(u[self.source], 0, atol=0.01):
        """
        if step % 100 == 0:
            u_next[self.source] = 1.0  # Repeat pulse
            print("pulse")
        """
        if self.source is not None and self.source_active:
            u_next[self.source] = math.sin(2 * math.pi * step * source_freq)

        # Rotate; `next` will be overwritten but this avoids memory allocation
        u, u_1, u_next = u_next, u, u_1
        # Copy state to members
        self.u, self.u_1, self.u_next = u, u_1, u_next

    def update_wave_vec(self, step):
        """Vectorized version of update.
        Doesn't work yet...
        """
        rsq = velocity**2 * time_step**2
        # Update displacement using wave equation
        u[1:-1] += rsq * (u[:-2] - 2 * u[1:-1] + u[2:])

        # Refactoring
        tmp = u
        u += 2 * (1 - rsq) * u[a] - u1[a] + rsq * (u[a - 1] + u[a + 1])

        u += 2 * u[a] - 2 * rsq * u[a] + rsq * (u[a - 1] + u[a + 1]) - u1[a]

        u1 = tmp
        # u1, u = u, tmp

        # Apply damping
        u *= 1 - self.damping_factor * time_step
        # Boundary conditions (fixed ends)
        u[0] = 0
        u[-1] = 0

    def draw(self, img):
        for i in range(self.num_points):
            x, y = np.intp((4 * i, 100 * self.u[i] + height / 2))
            cv2.circle(img, (x, y), radius=4, color=(0, 0, 255), thickness=-1)


def main():
    wavesim = WaveSim(num_points, source=source_0, crossed_points=crossed_points)
    wavesim.source_active = True
    img = np.full((height, width, num_channels), (0, 0, 0), dtype=np.uint8)
    t = 0
    while True:
        t += 1
        # print(f"===== {step}")
        # if step == 1:
        #    print(u)
        wavesim.update_wave(t)
        img *= 0
        wavesim.draw(img)
        cv2.imshow("lights", img)
        if cv2.waitKey(1) == ord("q"):
            cv2.destroyAllWindows()
            break


if __name__ == "__main__":
    main()
