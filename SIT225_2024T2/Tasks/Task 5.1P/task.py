import firebase_admin
import pandas as pd
import matplotlib.pyplot as plt
import serial
import time
from firebase_admin import credentials, db

cred_obj = credentials.Certificate("task-5-1p-28c7b-firebase-adminsdk-fbsvc-74e02b043e.json")
databaseURL = 'https://task-5-1p-28c7b-default-rtdb.firebaseio.com/'
default_app = firebase_admin.initialize_app(cred_obj, {'databaseURL': databaseURL})

def read_from_arduino():
    ser = serial.Serial('/dev/cu.usbmodem101', 9600)  # Change based on your system
    time.sleep(2)  # Allow connection time
    
    data_list = []
    ref = db.reference("/gyroscope_data")  # <-- Move this inside the function

    print("Reading data from Arduino...")
    try:
        for _ in range(1800):  # Collect data for 30 minutes (1 sample per sec)
            raw_data = ser.readline().decode('utf-8').strip()
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

            if raw_data.count(',') == 2:  # Ensure correct data format
                try:
                    x, y, z = map(float, raw_data.split(','))
                    data = {
                        "x": x,
                        "y": y,
                        "z": z
                    }
                    ref.child(timestamp).set(data)  # Store with timestamp as key
                    data_list.append({"timestamp": timestamp, "x": x, "y": y, "z": z})
                    print(data)
                except ValueError:
                    print(f"Ignored invalid data: {raw_data}")
            else:
                print(f"Ignored invalid data: {raw_data}")
            
            time.sleep(20)

    except KeyboardInterrupt:
        print("Data collection stopped manually.")

    finally:
        ser.close()
        save_to_csv(data_list)

def save_to_csv(data_list):
    df = pd.DataFrame(data_list)
    df.to_csv("gyroscope_data.csv", index=False)
    print("Data saved to gyroscope_data.csv")

if __name__ == "__main__":
    read_from_arduino()
    