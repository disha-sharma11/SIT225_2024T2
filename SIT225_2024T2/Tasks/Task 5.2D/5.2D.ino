#include <WiFiNINA.h>
#include <PubSubClient.h>
#include <Arduino_LSM6DS3.h>

// WiFi Credentials
char ssid[] = "Disha";
char pass[] = "12345678";

// HiveMQ Credentials
const char* mqtt_broker = "fe286e37150e421ca82a491adb670949.s1.eu.hivemq.cloud";
const int mqtt_port = 8883;  // ✅ Use 8883 (SSL)
const char* mqtt_username = "hivemq.webclient.1742035249339";
const char* mqtt_password = "Ey6v80qF9iCAlkBD%$,.";
const char* mqtt_topic = "gyroscope/data";

WiFiSSLClient wifiClient;
PubSubClient client(wifiClient);

void setup() {
  Serial.begin(115200);
  while (!Serial)
    ;

  Serial.println("Connecting to Wi-Fi...");
  WiFi.begin(ssid, pass);

  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 15) {
    delay(1000);
    Serial.print(".");
    attempts++;
  }
  Serial.flush();
  delay(2000);

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\n✅ Connected to Wi-Fi!");
    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\n❌ Failed to connect to Wi-Fi!");
  }

  // ✅ Reconnect WiFi if Lost
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("\n❌ WiFi Lost. Waiting...");
    delay(5000);  // Give it time to auto-reconnect
    if (WiFi.status() != WL_CONNECTED) {
      Serial.println("🔄 Manual Reconnect Attempt...");
      WiFi.begin(ssid, pass);
    }
  }

  Serial.print("WiFi Status Before MQTT: ");
  Serial.println(WiFi.status());

  // ✅ Enable SSL for MQTT
  // wifiClient.setInsecure();  // Skip certificate verification

  // ✅ Ensure MQTT Client is Ready
  client.setServer(mqtt_broker, mqtt_port);
  client.loop();  

  Serial.print("Connecting to MQTT...");
  while (!client.connected()) {
    if (client.connect("ArduinoClient", mqtt_username, mqtt_password)) {
      Serial.println("\n✅ Connected to MQTT!");
    } else {
      Serial.print(".");
      delay(1000);
    }
  }

  Serial.print("WiFi Status After MQTT: ");
  Serial.println(WiFi.status());

  // ✅ Initialize Gyroscope Sensor
  if (!IMU.begin()) {
    Serial.println("❌ Failed to initialize IMU!");
    return;
  }
  Serial.println("✅ Gyroscope Ready");
}

void loop() {
  if (IMU.gyroscopeAvailable()) {
    float gyroX, gyroY, gyroZ;
    IMU.readGyroscope(gyroX, gyroY, gyroZ);
    delay(100);

    // ✅ Create MQTT message
    String payload = String(gyroX) + "," + String(gyroY) + "," + String(gyroZ);
    client.publish(mqtt_topic, payload.c_str());

    Serial.println("📤 Published: " + payload);
  }

  client.loop();
  delay(1000);
}
