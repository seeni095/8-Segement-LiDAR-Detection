#!/usr/bin/env python3

import numpy as np
from collections import deque

# Placeholder for your baseline samples (collected facing flat surface)
baseline_samples = [
    [2.65, 2.37, 2.18, 2.08, 2.08, 2.25, 2.49, 2.9],  # Example raw samples
    [2.66, 2.38, 2.17, 2.09, 2.08, 2.26, 2.48, 2.89],
    [2.64, 2.36, 2.19, 2.08, 2.09, 2.24, 2.50, 2.91],
]
baseline_samples = np.array(baseline_samples)

# Compute average distance per beam
avg_baseline = baseline_samples.mean(axis=0)

# Symmetrize using geometric U-shape assumption (beam 0 = 7, 1 = 6, etc.)
sym_baseline = avg_baseline.copy()
pairs = [(0,7), (1,6), (2,5), (3,4)]
for i, j in pairs:
    mean_val = (avg_baseline[i] + avg_baseline[j]) / 2.0
    sym_baseline[i] = sym_baseline[j] = mean_val

# Compute per-segment calibration offsets
offsets = avg_baseline - sym_baseline

# Moving average window per beam (length = 5)
window_size = 5
beam_windows = [deque(maxlen=window_size) for _ in range(8)]

def calibrate_and_filter(raw_readings):
    """
    Calibrates and filters 8-beam raw LiDAR readings.
    Input: raw_readings – list or np.array of 8 raw distances
    Returns: list of 8 calibrated and smoothed distances
    """
    raw = np.array(raw_readings)
    calibrated = raw - offsets

    # Outlier filter – replace spikes based on neighbors
    for i in range(8):
        if 0 < i < 7:
            neighbor_avg = 0.5 * (calibrated[i-1] + calibrated[i+1])
            if abs(calibrated[i] - neighbor_avg) > 0.1:
                calibrated[i] = neighbor_avg

    # Apply moving average smoothing
    smoothed = []
    for i in range(8):
        beam_windows[i].append(calibrated[i])
        smoothed.append(np.mean(beam_windows[i]))

    return smoothed

# Example usage
if __name__ == "__main__":
    # Simulated incoming frame from Vu8
    raw_frame = [2.68, 2.35, 2.16, 2.09, 2.10, 2.26, 2.51, 2.89]
    calibrated_output = calibrate_and_filter(raw_frame)
    print("Calibrated & Smoothed Output:", calibrated_output)
