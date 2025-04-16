import sys
import traceback
import time
from arduino_iot_cloud import ArduinoCloudClient

# Replace with your actual Arduino IoT Cloud credentials
DEVICE_ID = "8804f551-ab6a-4878-9b3d-9beae644d0e7"  
SECRET_KEY = "nl49dbaA4#Y#hQe8N9JArkMyx"
USERNAME = DEVICE_ID  # Using the device ID as username

# CSV file path for combined accelerometer data
FILE_DATA = "accelerometer_data.csv"

# Write header to CSV file (if not already present)
with open(FILE_DATA, mode='a', newline='') as file:
    file.write("Timestamp,AccelerometerX,AccelerometerY,AccelerometerZ\n")

# Global dictionaries to store sensor values and update flags
sensor_data = {"x": None, "y": None, "z": None}
updated = {"x": False, "y": False, "z": False}

def log_if_ready():
    """Log data to CSV once all three sensor values have been updated."""
    if updated["x"] and updated["y"] and updated["z"]:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        line = f"{timestamp},{sensor_data['x']},{sensor_data['y']},{sensor_data['z']}\n"
        with open(FILE_DATA, mode='a', newline='') as f:
            f.write(line)
            f.flush()
        print(f"Logged Data: {line.strip()}")
        # Reset update flags so the next set of values can be gathered
        updated["x"] = updated["y"] = updated["z"] = False

def on_accelerometer_x_changed(client, value):
    sensor_data["x"] = value
    updated["x"] = True
    log_if_ready()

def on_accelerometer_y_changed(client, value):
    sensor_data["y"] = value
    updated["y"] = True
    log_if_ready()

def on_accelerometer_z_changed(client, value):
    sensor_data["z"] = value
    updated["z"] = True
    log_if_ready()

def main():
    print("Initializing Arduino Cloud client for accelerometer data...")
    client = ArduinoCloudClient(
        device_id=DEVICE_ID, username=USERNAME, password=SECRET_KEY
    )
    
    # Register accelerometer variables with their names (as defined in Arduino Cloud)
    client.register(
        "accelerometerX", value=None,
        on_write=on_accelerometer_x_changed
    )
    client.register(
        "accelerometerY", value=None,
        on_write=on_accelerometer_y_changed
    )
    client.register(
        "accelerometerZ", value=None,
        on_write=on_accelerometer_z_changed
    )
    
    client.start()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Error occurred:", e)
        traceback.print_exc()
