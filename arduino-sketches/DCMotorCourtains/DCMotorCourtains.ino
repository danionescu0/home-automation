#include <SoftwareSerial.h>

const byte pwmPower = 160;
const byte powerPwmPin = 9;
const byte relay1StatePin = 8;
const byte relay2StatePin = 7;

SoftwareSerial bluetooth(10, 11); // RX, TX
char buffer[] = {' ',' ',' '};

void setup() 
{
    Serial.begin(9600);
    bluetooth.begin(9600);
    pinMode(powerPwmPin, OUTPUT);
    pinMode(relay1StatePin , OUTPUT);
    pinMode(relay2StatePin, OUTPUT);
    digitalWrite(powerPwmPin, LOW);
    digitalWrite(relay1StatePin, LOW);
    digitalWrite(relay2StatePin, LOW);   
}

void loop() 
{
  if (bluetooth.available() > 0) {   
      bluetooth.readBytesUntil(';', buffer, 4);
      toggleState(getState(), getDuration());
      clearBuffer();  
  } 
}

boolean getState()
{
    return buffer[0] == 'C' ? false : true;
}

byte getDuration()
{
    String value = "";
    value += String(buffer[1]) + String(buffer[2]);

    return (byte) value.toInt();
}

void toggleState(boolean state, byte duration)
{  
    Serial.print("State:");Serial.println(state);
    Serial.print("Duration:");Serial.println(duration);
    if (state) {
        digitalWrite(relay1StatePin, HIGH);
        digitalWrite(relay2StatePin, HIGH);        
    } else {
        digitalWrite(relay1StatePin, LOW);
        digitalWrite(relay2StatePin, LOW);        
    }
    analogWrite(powerPwmPin, pwmPower);
    long millisecondsSleep = (long) duration * 1000;
    delay(millisecondsSleep);
    digitalWrite(powerPwmPin, LOW);
}

void clearBuffer()
{
    for (int i=0; i<=2; i++) {
        buffer[i] = ' ';
    }
}

