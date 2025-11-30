void setup() {
  Serial.begin(9600);
}

void loop() {
  static int v = 0;
  Serial.println(v);
  v = (v + 1) % 256;
  delay(20);
}
