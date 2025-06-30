# 8-Segment LiDAR Flap Detection and Calibration

This repository contains Python scripts and sample data used in the paper:
**"Calibrating 1D LiDAR for Accurate UAV Flap Detection"** (submitted to Optical Engineering, SPIE).

## 📌 Description

This project implements a calibration and filtering pipeline for the 8-segment solid-state Leddar Vu8 LiDAR sensor to detect flap deflections in UAVs. The algorithm aligns raw LiDAR data to a theoretical U-profile to improve detection accuracy and eliminate sensor bias and noise.

## 📂 Repository Contents

- `calibrate_and_filter.py`: Core calibration and smoothing algorithm
- `raw_data.csv`: Example raw LiDAR readings (before calibration)
- `calibrated_output.csv`: Output after calibration
- `baseline_profile.csv`: Theoretical distances for a flat surface
- `README.md`: This file

## ⚙️ Dependencies

- Python 3.8+
- `numpy`
- `collections` (built-in)

Install dependencies:
```bash
pip install numpy
