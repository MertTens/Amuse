#include <Servo.h>

Servo myservo;

int servoPos = 0;
int incomingByte;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  myservo.attach(9);
}

void loop() {
  // put your main code here, to run repeatedly:

  while(Serial.available() == 0){
    
  }

  incomingByte = int(Serial.parseInt());

  if(incomingByte != 0){
    
//    Serial.print("Writing to servo int: ");
//    Serial.println(incomingByte);
    
    myservo.write(incomingByte);
  }
}
