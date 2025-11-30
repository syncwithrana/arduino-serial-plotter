#include <Wire.h>
#include <SoftwareWire.h>

// Software I2C Master on pins 8 (SDA) and 9 (SCL)
SoftwareWire swWire(8, 9);

// Slave receives here:
volatile uint8_t lastByte = 0;

void onReceiveHandler(int count) {
  while (Wire.available()) {
    lastByte = Wire.read();
    Serial.print("Slave RX: ");
    Serial.println(lastByte);
  }
}

void setup() {
  Serial.begin(9600);

  // Hardware I2C slave
  Wire.begin(0x42);
  Wire.onReceive(onReceiveHandler);

  // Software master
  swWire.begin();

  Serial.println("Self I2C test: Master->Slave");
}

void loop() {
  static uint8_t v = 0;

  // Master sends 1 byte to slave 0x42
  swWire.beginTransmission(0x42);
  swWire.write(v);
  swWire.endTransmission();

  Serial.print("Master TX: ");
  Serial.println(v);

  v = (v + 1) % 256;

  delay(100);
}
