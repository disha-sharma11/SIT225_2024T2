import serial
import time
import csv

# Set baud rate, same speed as set in Arduino
baud_rate = 9600

# Set serial port (change this as per your system)
s = serial.Serial('/dev/cu.usbmodem101', baud_rate, timeout=5)

# Open CSV file
file_name = "dht22_data.csv"
with open(file_name, "a", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Timestamp", "Temperature (°C)", "Humidity (%)"])  # Column headers

    while True:

            # Read data from Arduino
            data_recv = s.readline().decode('utf-8').strip()
            
            if data_recv and "Error" not in data_recv:
                millis, temp, hum = data_recv.split(",")
                
                # Generate timestamp
                timestamp = time.strftime("%Y%m%d%H%M%S")
                
                # Save to CSV
                writer.writerow([timestamp, temp, hum])
                print(f"Saved to CSV: {timestamp}, {temp}°C, {hum}%")


