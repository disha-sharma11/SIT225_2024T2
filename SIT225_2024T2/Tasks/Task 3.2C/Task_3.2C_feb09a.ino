#include "arduino_secrets.h"
/* 
  Sketch generated by the Arduino IoT Cloud Thing "Task 3.1P"
  https://create.arduino.cc/cloud/things/93d664d8-242f-4248-a649-305640cd3ede 

  Arduino IoT Cloud Variables description

  The following variables are automatically generated and updated when changes are made to the Thing

  float accelX;
  float accelY;
  float accelZ;
  bool alarmTriggered;

  Variables which are marked as READ/WRITE in the Cloud Thing will also have functions
  which are called when their values are changed from the Dashboard.
  These functions are generated with the Thing and added at the end of this sketch.
*/

#include "thingProperties.h"
#include <Arduino_LSM6DS3.h>

float x, y, z;

void setup() {
  Serial.begin(9600);
  while (!Serial);
  Serial.println("Started");

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }

  Serial.println("Accelerometer sample rate = " + String(IMU.accelerationSampleRate()) + " Hz");

  initProperties();
  ArduinoCloud.begin(ArduinoIoTPreferredConnection);
}

void loop() {
  ArduinoCloud.update();

  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(x, y, z);
    Serial.println(String(x) + ", " + String(y) + ", " + String(z));

    // Check for sudden movement (modify thresholds as needed)
    if (abs(x) > 2.0 || abs(y) > 2.0 || abs(z) > 2.0) {  
      alarmTriggered = true; 
      Serial.println("ALARM TRIGGERED!");
    }
  }

  delay(1000);
}



/*
  Since AccelX is READ_WRITE variable, onAccelXChange() is
  executed every time a new value is received from IoT Cloud.
*/
void onAccelXChange()  {
  // Add your code here to act upon AccelX change
}

/*
  Since AccelY is READ_WRITE variable, onAccelYChange() is
  executed every time a new value is received from IoT Cloud.
*/
void onAccelYChange()  {
  // Add your code here to act upon AccelY change
}

/*
  Since AccelZ is READ_WRITE variable, onAccelZChange() is
  executed every time a new value is received from IoT Cloud.
*/
void onAccelZChange()  {
  // Add your code here to act upon AccelZ change
}




/*
  Since AlarmTriggered is READ_WRITE variable, onAlarmTriggeredChange() is
  executed every time a new value is received from IoT Cloud.
*/
void onAlarmTriggeredChange()  {
  // Add your code here to act upon AlarmTriggered change
}

