#include <SoftwareSerial.h>

const int courtain1dirPin1 = 5;
const int courtain1dirPin2 = 6;
const int courtain2dirPin1 = 7;
const int courtain2dirPin2 = 8;
const int courtain1EnablePin = 3;
const int courtain2EnablePin = 9;
const unsigned long onState = 1;
const unsigned long offState = 0;
const unsigned long changeStateMillis = 80000;
const int courtain1PWM = 120;
const int courtain2PWM = 120;

SoftwareSerial bluetooth(10, 11); // RX, TX

void setup() 
{
    Serial.begin(9600);
    bluetooth.begin(9600);
    pinMode(courtain1dirPin1, OUTPUT);
    pinMode(courtain1dirPin2 , OUTPUT);
    pinMode(courtain1EnablePin, OUTPUT);
    digitalWrite(courtain1dirPin1, HIGH);
    digitalWrite(courtain1dirPin2, LOW);
    digitalWrite(courtain1EnablePin, LOW);
    pinMode(courtain2dirPin1, OUTPUT);
    pinMode(courtain2dirPin2 , OUTPUT);
    pinMode(courtain2EnablePin, OUTPUT);
    digitalWrite(courtain2dirPin1, HIGH);
    digitalWrite(courtain2dirPin2, LOW);
    digitalWrite(courtain2EnablePin, LOW);   
    Serial.println("done with init");
    bluetooth.println("test");
}

void loop() 
{
  if (bluetooth.available() > 0) {   
      int received = bluetooth.read() - 48;
      Serial.println(received);   
      delay(100);
      toggleState(received);  
  } 
}

void toggleState(int received)
{
    if (received == offState) {
        Serial.println("on");
        digitalWrite(courtain1dirPin1, HIGH);
        digitalWrite(courtain1dirPin2, LOW);   
        digitalWrite(courtain2dirPin1, HIGH);
        digitalWrite(courtain2dirPin2, LOW);
        analogWrite(courtain1EnablePin, courtain1PWM);
        analogWrite(courtain2EnablePin, courtain2PWM);                  
    } else if (received == onState) {
        Serial.println("off");
        digitalWrite(courtain1dirPin1, LOW);
        digitalWrite(courtain1dirPin2, HIGH);   
        digitalWrite(courtain2dirPin1, LOW);
        digitalWrite(courtain2dirPin2, HIGH);
        analogWrite(courtain1EnablePin, courtain1PWM);
        analogWrite(courtain2EnablePin, courtain2PWM);                            
    } 
    delay(changeStateMillis);    
    digitalWrite(courtain1EnablePin, LOW);    
    digitalWrite(courtain2EnablePin, LOW);    
}
