#include <Servo.h>

Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;
Servo servo5;
Servo servo6;
Servo servo7;  // New servo

int angles[7];  // Updated array size to 7
int currentAngles[7];  // Updated array size to 7
float speed;  // Speed in degrees per second

void setup() {
  Serial.begin(9600);
  servo1.attach(9);  // Attach servos to pins
  servo2.attach(10);
  servo3.attach(3);
  servo4.attach(4);
  servo5.attach(5);
  servo6.attach(6);
  servo7.attach(7);  // Attach the new servo

  // Initialize current angles
  currentAngles[0] = servo1.read();
  currentAngles[1] = servo2.read();
  currentAngles[2] = servo3.read();
  currentAngles[3] = servo4.read();
  currentAngles[4] = servo5.read();
  currentAngles[5] = servo6.read();
  currentAngles[6] = servo7.read();  // Initialize the new servo
}

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');  // Read data until newline character
    parseData(data);
    updateServos();
  }
}

void parseData(String data) {
  int commaIndex = 0;
  int startIndex = 0;
  
  // Parse angles
  for (int i = 0; i < 7; i++) {
    commaIndex = data.indexOf(',', startIndex);
    angles[i] = data.substring(startIndex, commaIndex).toInt();
    startIndex = commaIndex + 1;
  }
  
  // Parse speed
  speed = data.substring(startIndex).toFloat();
}

void updateServos() {
  bool anglesUpdated = true;
  
  while (anglesUpdated) {
    anglesUpdated = false;
    for (int i = 0; i < 7; i++) {
      if (currentAngles[i] < angles[i]) {
        currentAngles[i]++;
        anglesUpdated = true;
      } else if (currentAngles[i] > angles[i]) {
        currentAngles[i]--;
        anglesUpdated = true;
      }
    }

    // Update servo positions
    servo1.write(currentAngles[0]);
    servo2.write(180 - currentAngles[1]);
    servo3.write(currentAngles[1]);  // Keep servo2 and servo3 in sync
    servo4.write(currentAngles[3]);
    servo5.write(currentAngles[4]);
    servo6.write(currentAngles[5]);
    servo7.write(currentAngles[6]);  // Update the new servo

    delay(1000 / speed);  // Delay based on speed
  }

  // Ensure final angles are reached
  servo1.write(angles[0]);
  servo2.write(180 - angles[1]);
  servo3.write(angles[1]);  // Keep servo2 and servo3 in sync
  servo4.write(angles[3]);
  servo5.write(angles[4]);
  servo6.write(angles[5]);
  servo7.write(angles[6]);  // Ensure the new servo reaches its final angle
}

