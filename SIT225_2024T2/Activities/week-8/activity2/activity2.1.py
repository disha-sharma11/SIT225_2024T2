import sys
import traceback
import time
from arduino_iot_cloud import ArduinoCloudClient

# Replace with your actual Arduino IoT Cloud credentials
DEVICE_ID = "8804f551-ab6a-4878-9b3d-9beae644d0e7"  
SECRET_KEY = "nl49dbaA4#Y#hQe8N9JArkMyx"
# Use the device ID as the username (this is common with Arduino Cloud Python libraries)
USERNAME = DEVICE_ID  

# CSV file paths
FILE_X = "accelerometer_x.csv"
FILE_Y = "accelerometer_y.csv"
FILE_Z = "accelerometer_z.csv"

# Write headers to CSV files (if not already present)
for file_path, header in [
    (FILE_X, "Timestamp,AccelerometerX\n"),
    (FILE_Y, "Timestamp,AccelerometerY\n"),
    (FILE_Z, "Timestamp,AccelerometerZ\n")
]:
    with open(file_path, mode='a', newline='') as file:
        file.write(header)

def on_accelerometer_x_changed(client, value):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    csv_string = f"{timestamp},{value}\n"
    with open(FILE_X, mode='a', newline='') as file:
        file.write(csv_string)
        file.flush()
    print(f"Logged AccelerometerX: {csv_string.strip()}")

def on_accelerometer_y_changed(client, value):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    csv_string = f"{timestamp},{value}\n"
    with open(FILE_Y, mode='a', newline='') as file:
        file.write(csv_string)
        file.flush()
    print(f"Logged AccelerometerY: {csv_string.strip()}")

def on_accelerometer_z_changed(client, value):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    csv_string = f"{timestamp},{value}\n"
    with open(FILE_Z, mode='a', newline='') as file:
        file.write(csv_string)
        file.flush()
    print(f"Logged AccelerometerZ: {csv_string.strip()}")

def main():
    print("Initializing Arduino Cloud client for accelerometer data...")
    
    client = ArduinoCloudClient(
        device_id=DEVICE_ID, username=USERNAME, password=SECRET_KEY
    )
    
    # Registering accelerometer variables by their names (exactly as defined in Arduino Cloud)
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
