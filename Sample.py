#!/usr/bin/env python3
import leddar
import time
import csv

def echoes_callback(echoes):
    data = echoes["data"]
    print("Received new echo data, writing to CSV...")
    with open('echoes_data.csv', 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        for echo in data:
            csv_writer.writerow([
                echo["indices"],
                echo["distances"],
                echo["amplitudes"],
                echo["flags"],
                echo["x"],
                echo["y"],
                echo["z"],
                echoes['timestamp']
            ])

# Initialize device and connect using Serial (USB)
device = leddar.Device()
# Connect using serial port /dev/ttyACM0
if not device.connect('/dev/ttyACM0', leddar.device_types["Serial"]):
    print("Failed to connect to the device.")
    exit(1)

# Setup data mask and callbacks
device.set_callback_echo(echoes_callback)
device.set_data_mask(leddar.data_masks["DM_ECHOES"])
device.start_data_thread()

# Write header to the CSV file
with open('echoes_data.csv', 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["Indices", "Distance", "Amplitude", "Flag", "X", "Y", "Z", "Timestamp"])

# Collect data for a specified duration
try:
    print("Collecting data. Press Ctrl+C to stop.")
    time.sleep(30)
except KeyboardInterrupt:
    print("Data collection interrupted by user.")

# Cleanup
device.stop_data_thread()
device.disconnect()
print("Disconnected from the device.")
