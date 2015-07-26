#include <SoftwareSerial.h>
#include <Wire.h>
#include "HTU21D.h"

SoftwareSerial bt1(6, 5); // RX, TX
HTU21D tempHumid;

void setup() 
{
  bt1.begin(9600);
  Serial.begin(9600);
  tempHumid.begin();
}

void loop() 
{
  int humd = tempHumid.readHumidity();
  int temp = tempHumid.readTemperature();
  int light = analogRead(A1);
  light =  map(light, 0, 1023, 0, 100);  
  bt1.print("H:");
  bt1.print(humd);
  bt1.print("|L:");
  bt1.print(light);
  bt1.print("|T:");  
  bt1.print(temp);
  bt1.print("|");
  Serial.print("Humid:");
  Serial.println(humd);
  Serial.print("Temp:");
  Serial.println(temp);  
  Serial.print("Light:");
  Serial.println(light);
  delay(60000);        
}
