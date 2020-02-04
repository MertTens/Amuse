#include <Servo.h>

Servo myservo;

int servoPos = 0;
int incomingByte;

void setup() {
  // put your setup code here, to run once:

  pinMode(11, OUTPUT);
  Serial.begin(9600);
  myservo.attach(11);
}

void loop() {
  // put your main code here, to run repeatedly:

  while(Serial.available() == 0){
    
  }

  incomingByte = int(Serial.parseInt());

  if(incomingByte == 2){
    myservo.write(90);
  }
  else if(incomingByte == 3){
    myservo.write(45);
  }
}
