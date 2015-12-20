#include <RCSwitch.h>

RCSwitch mySwitch = RCSwitch();

const int courtain1dirPin1 = 5;
const int courtain1dirPin2 = 6;
const int courtain2dirPin1 = 7;
const int courtain2dirPin2 = 8;
const int courtain1EnablePin = 3;
const int courtain2EnablePin = 9;
const unsigned long openRcState = 1397845;
const unsigned long closedRcState = 1397844;
const unsigned int onStateMillis = 36000;
const unsigned int offStateMillis = 38000;
const int courtain1PWM = 210;
const int courtain2PWM = 252;

void setup() 
{
    Serial.begin(9600);
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
    mySwitch.enableReceive(0);
}

void loop() 
{
  if (mySwitch.available()) {    
      unsigned long value = mySwitch.getReceivedValue();
      Serial.println(value);
      delay(100);
      toggleState(value);
      mySwitch.resetAvailable();    
  } 
}

void toggleState(unsigned long rcCode)
{
    if (rcCode == openRcState) {
        Serial.println("on");
        digitalWrite(courtain1dirPin1, HIGH);
        digitalWrite(courtain1dirPin2, LOW);   
        digitalWrite(courtain2dirPin1, HIGH);
        digitalWrite(courtain2dirPin2, LOW);
        analogWrite(courtain1EnablePin, courtain1PWM);
        analogWrite(courtain2EnablePin, courtain2PWM);
        delay(onStateMillis);                    
    } else if (rcCode == closedRcState) {
         Serial.println("off");
        digitalWrite(courtain1dirPin1, LOW);
        digitalWrite(courtain1dirPin2, HIGH);   
        digitalWrite(courtain2dirPin1, LOW);
        digitalWrite(courtain2dirPin2, HIGH);
        analogWrite(courtain1EnablePin, courtain1PWM);
        analogWrite(courtain2EnablePin, courtain2PWM);        
        delay(offStateMillis);                    
    } 
    digitalWrite(courtain1EnablePin, LOW);    
    digitalWrite(courtain2EnablePin, LOW);    
}
