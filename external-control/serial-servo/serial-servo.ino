#include <Servo.h>

Servo myservo;

int servoPos = 0;
int incomingByte;
int servoPin = 9;

void setup() {
  // put your setup code here, to run once:

  pinMode(servoPin, OUTPUT);
  Serial.begin(9600);
  myservo.attach(servoPin);
}

void loop() {
  // put your main code here, to run repeatedly:

  while(Serial.available() == 0){
    
  }

  incomingByte = int(Serial.parseInt());

//  if(incomingByte == 2){
//    myservo.write(90);
//  }
//  else if(incomingByte == 3){
//    myservo.write(45);
//  }
  
  if(incomingByte != 0){
    
    Serial.print("Writing to servo int: ");
    Serial.println(incomingByte);
    
    myservo.write(incomingByte);
  }
}
