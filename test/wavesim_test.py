import numpy as np
import pytest
import sys

from pathlib import Path

sys.path.insert(0, str(Path(".").resolve()))

# This project
import wavesim


def test_zero_damping():
    NUM_POINTS = 100
    wave = wavesim.WaveSim(NUM_POINTS)
    wave.damping_factor = 0
    wave.u[1] = wave.u[2] = wave.u[3] = wave.u[NUM_POINTS - 4] = wave.u[
        NUM_POINTS - 3
    ] = wave.u[NUM_POINTS - 2] = 1
    wave.set_velocity(0.2)

    energy_0 = np.sum(wave.u)
    assert energy_0 == pytest.approx(6)

    for i in range(10000):
        wave.update_wave(0)
        # print(np.sum(wave.u))

    energy_n = np.sum(wave.u)

    assert energy_n != pytest.approx(0)
