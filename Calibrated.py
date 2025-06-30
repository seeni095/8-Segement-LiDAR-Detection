#!/usr/bin/env python3
from calibrate_and_filter import calibrate_and_filter
import os
import leddar
import time
import rospy
import subprocess
from sensor_msgs.msg import PointCloud2, PointField
import std_msgs.msg
import numpy as np
import sensor_msgs.point_cloud2 as pc2

leddar.enable_debug_trace(True)

# Callback functions for the data thread
def echoes_callback(echoes):
    data = echoes["data"]
    raw_distances = []

for point in data:
    raw_distances.append(point["distances"])

# Only process if 8 segments are detected
if len(raw_distances) == 8:
    calibrated_output = calibrate_and_filter(raw_distances)
    print("Calibrated Output:", calibrated_output)
else:
    print(f"Warning: Expected 8 segments, got {len(raw_distances)}")
    points = []

    for point in data:
        x = point["x"]
        y = point["y"]
        z = point["z"]
        points.append([x, y, z])

    header = std_msgs.msg.Header()
    header.stamp = rospy.Time.now()
    header.frame_id = 'map'

    fields = [
        PointField('x', 0, PointField.FLOAT32, 1),
        PointField('y', 4, PointField.FLOAT32, 1),
        PointField('z', 8, PointField.FLOAT32, 1),
    ]

    point_cloud = pc2.create_cloud(header, fields, points)
    pub.publish(point_cloud)

    # Original print statements for debugging
    increment = 1
    if len(data) > 100:
        increment = 100

    print("Count:" + str(len(data)))
    print("timestamp:" + str(echoes['timestamp']))

    row = ["Indices", "Distance", "Amplitude", "Flag", "X", "Y", "Z", "Timestamp"]
    print("{: <10} {: <15} {: <15} {: <5} {: <15} {: <15} {: <15} {: <15}".format(*row))
    for i in range(0, len(data), increment):
        row = [str(data[i]["indices"]), str(data[i]["distances"]), str(data[i]["amplitudes"]), str(data[i]["flags"]), str(data[i]["x"]), str(data[i]["y"]), str(data[i]["z"]), str(data[i]["timestamps"])]
        print("{: <10} {: <15} {: <15} {: <5} {: <15} {: <15} {: <15} {: <15}".format(*row))

def states_callback(states):
    print("timestamp: " + str(states["timestamp"]))
    print("cpu_load " + str(states["cpu_load"]) + "%")
    print("system_temp " + str(states["system_temp"]) + " C")

def exception_callback(exception):
    print(exception)

# Global device variable
dev = leddar.Device()

# Connect to the device
sensor_list = leddar.get_devices("Serial")
dev.connect('/dev/ttyACM0', leddar.device_types["Serial"])

# Get properties value
print("ID_DEVICE_NAME = " + dev.get_property_value(leddar.property_ids["ID_DEVICE_NAME"]))
print("ID_SERIAL_NUMBER = " + dev.get_property_value(leddar.property_ids["ID_SERIAL_NUMBER"]))

# Property available values
values = dev.get_property_available_values(leddar.property_ids["ID_DISTANCE_SCALE"])
print(values["type"])
print(values["data"])

# Set callback method
dev.set_callback_state(states_callback)
dev.set_callback_echo(echoes_callback)
dev.set_callback_exception(exception_callback)
dev.set_data_mask(leddar.data_masks["DM_STATES"] | leddar.data_masks["DM_ECHOES"])

# Optional: set the delay between two requests to the sensor
dev.set_data_thread_delay(10000)

def main():
    global dev
    global pub

    rospy.init_node('leddar_vu8_publisher')

    # Start RViz directly
    print("Starting RViz...")
    try:
        rviz_process = subprocess.Popen(['rviz'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"RViz started with PID {rviz_process.pid}")
    except Exception as e:
        print(f"Failed to start RViz: {e}")
        return

    # Create a publisher for the point cloud
    pub = rospy.Publisher('/point_cloud', PointCloud2, queue_size=10)

    # Start the Leddar device data thread
    dev.start_data_thread()

    try:
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
    finally:
        dev.stop_data_thread()
        dev.disconnect()
        del dev
        print("Terminating RViz...")
        rviz_process.terminate()
        rviz_process.wait()
        print("RViz terminated")

if __name__ == '__main__':
    main()
