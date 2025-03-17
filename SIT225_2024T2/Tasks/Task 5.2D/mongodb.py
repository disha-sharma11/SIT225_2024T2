import os
import json
import re
import ssl
import time
import paho.mqtt.client as mqtt
import pymongo
from datetime import datetime

# Load credentials from environment variables
MQTT_BROKER = "fe286e37150e421ca82a491adb670949.s1.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_TOPIC = "gyroscope"
MQTT_USERNAME = "Dishasharma1234"
MQTT_PASSWORD = "Dishasharma1234"
MONGO_URI = "mongodb+srv://dishasharma1234:dishasharnma1234@cluster0.qehoi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Validate credentials
if not all([MQTT_USERNAME, MQTT_PASSWORD, MONGO_URI]):
    raise ValueError("Missing required environment variables!")

# MongoDB Connection
try:
    mongo_client = pymongo.MongoClient(MONGO_URI)
    db = mongo_client["gyroscope_data"]
    collection = db["readings"]
    print("✅ Connected to MongoDB successfully!")
except Exception as e:
    print(f"❌ MongoDB Connection Error: {e}")
    exit()

def clean_sensor_data(raw_data):
    """
    Cleans and formats the raw sensor data into JSON format.
    """
    try:
        # Attempt to parse directly if it's already JSON
        parsed_data = json.loads(raw_data)
    except json.JSONDecodeError:
        # If not JSON, apply regex-based cleaning
        cleaned_data = re.sub(r"dps", "", raw_data).strip()
        cleaned_data = cleaned_data.replace("X:", '"x":').replace("Y:", '"y":').replace("Z:", '"z":')
        json_string = "{" + cleaned_data + "}"
        try:
            parsed_data = json.loads(json_string)
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON received: {raw_data}, Error: {e}")
            return None

    return parsed_data

def send_to_mongodb(data):
    """
    Inserts parsed data into MongoDB with a timestamp.
    """
    if data:
        data["timestamp"] = datetime.utcnow()
        collection.insert_one(data)
        print("✅ Data saved to MongoDB:", data)

def on_connect(client, userdata, flags, rc):
    """
    Handles MQTT broker connection.
    """
    if rc == 0:
        print("✅ Connected to MQTT Broker")
        client.subscribe(MQTT_TOPIC)
        print(f"📡 Subscribed to topic: {MQTT_TOPIC}")
    else:
        print(f"❌ Failed to connect to MQTT Broker, Return code {rc}")

def on_message(client, userdata, msg):
    """
    Handles incoming MQTT messages.
    """
    raw_data = msg.payload.decode("utf-8").strip()
    print(f"📩 Raw data received: {raw_data}")

    try:
        # If raw_data is already JSON, parse it directly
        parsed_data = json.loads(raw_data)
    except json.JSONDecodeError:
        # Handle case where raw_data is a CSV string
        try:
            x, y, z = map(float, raw_data.split(','))
            parsed_data = {"x": x, "y": y, "z": z}  # Convert to JSON format
        except ValueError:
            print(f"❌ Failed to parse data: {raw_data}")
            return  # Skip invalid data

    print(f"✅ Parsed JSON: {parsed_data}")
    # Now you can insert `parsed_data` into MongoDB

# Setup MQTT Client
mqtt_client = mqtt.Client()
mqtt_client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
mqtt_client.tls_set_context(ssl.create_default_context())  # Secure connection

mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# Connect to MQTT Broker
try:
    print("🔗 Connecting to MQTT Broker...")
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
    mqtt_client.loop_forever()  # Keep listening indefinitely
except Exception as e:
    print(f"❌ MQTT Connection Error: {e}")
