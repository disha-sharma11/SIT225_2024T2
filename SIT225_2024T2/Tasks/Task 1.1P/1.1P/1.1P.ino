int x;

void setup() {
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT); 
}

void loop() {
  while (!Serial.available()) {} // wait for data to arrive

  x = Serial.readString().toInt();
  Serial.flush();

  for (int i = 0; i < x; i++) {
    digitalWrite(LED_BUILTIN, HIGH);
    delay(1000);
    digitalWrite(LED_BUILTIN, LOW);
    delay(1000);
  }

  int randomNum = random(1, 10); 
  delay(500);
  Serial.println(randomNum);

}
