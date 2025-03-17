import json
import re
import paho.mqtt.client as mqtt
import ssl
from datetime import datetime, timezone
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# InfluxDB Configuration
INFLUXDB_URL = "https://us-east-1-1.aws.cloud2.influxdata.com"
INFLUXDB_TOKEN = "HOEhbU4gvKF0F0hdGw2JY5NrWbvl2Vjl2Nva4nTHVsFl-cA3SDm-tFfbVcaYiOymZf4W5nOkT8iWCywbSHzxxg=="
INFLUXDB_ORG = "Disha"
INFLUXDB_BUCKET = "GyroData"

# MQTT Configuration
MQTT_BROKER = "fe286e37150e421ca82a491adb670949.s1.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_TOPIC = "gyroscope"
MQTT_USERNAME = "Dishasharma1234"
MQTT_PASSWORD = "Dishasharma1234"

# Connect to InfluxDB
client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)

def clean_sensor_data(raw_data):
    try:
        # Split the raw data into three values
        values = raw_data.split(",")
        if len(values) != 3:
            raise ValueError("Unexpected data format")

        # Convert the values into a dictionary
        parsed_data = {
            "X": float(values[0]),
            "Y": float(values[1]),
            "Z": float(values[2])
        }
        return parsed_data
    except (ValueError, IndexError) as e:
        print(f"Invalid sensor data received: {raw_data}, Error: {e}")
        return None

def send_to_influxdb(data):
    if data:
        point = (
            Point("gyroscope_data")
            .field("X", float(data["X"]))
            .field("Y", float(data["Y"]))
            .field("Z", float(data["Z"]))
            .time(datetime.now(timezone.utc))
        )
        write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)
        print("Inserted into InfluxDB:", data)

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Connected to MQTT broker")
        client.subscribe(MQTT_TOPIC)
    else:
        print(f"Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    raw_data = msg.payload.decode("utf-8").strip()
    print("Raw data received:", raw_data)
    cleaned_json_data = clean_sensor_data(raw_data)
    if cleaned_json_data:
        send_to_influxdb(cleaned_json_data)

mqtt_client = mqtt.Client()
mqtt_client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
mqtt_client.tls_set_context(ssl.create_default_context())  
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

try:
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
    mqtt_client.loop_forever()
except Exception as e:
    print(f"Error: {e}")