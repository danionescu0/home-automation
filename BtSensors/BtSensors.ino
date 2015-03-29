#include <SoftwareSerial.h>
#include <Wire.h>
#include "HTU21D.h"

SoftwareSerial bt1(6, 5); // RX, TX
SoftwareSerial bt2(7, 8); // RX, TX
HTU21D myHumidity;

void setup() 
{
  bt1.begin(9600);
  bt2.begin(9600);
  Serial.begin(9600);
  myHumidity.begin();
  Serial.println("Begin");
}

void loop() 
{
  //int airQuality = analogRead(A0);
  Serial.println("1");
  int humd = myHumidity.readHumidity();
  Serial.println("2");
  int light = analogRead(A1);
  light =  map(light, 0, 1023, 1023, 0);  
  bt1.print(humd);
  bt1.print("|");
  bt2.print(light);
  bt2.print("|");  
  Serial.print("Air=");
  Serial.println(humd);
  Serial.print("Light=");
  Serial.println(light);
  delay(60000);        
}
