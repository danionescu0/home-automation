#include <SoftwareSerial.h>
#include <Wire.h>
#include "HTU21D.h"
#include <BH1750.h>

SoftwareSerial bt1(6, 5); // RX, TX
HTU21D tempHumid;
BH1750 lightMeter;

const int airQualitySenzorPin = A3;
long timeLastTransmitted;
boolean movementDetected = false;
const long transmitInterval = 60000;

void setup() 
{
  bt1.begin(9600);
  Serial.begin(9600);
  tempHumid.begin();
  lightMeter.begin();
  timeLastTransmitted = millis();
  
}

void loop() 
{
    int humd = tempHumid.readHumidity();
    int temp = tempHumid.readTemperature();
    int light = lightMeter.readLightLevel();
    int airQuality = analogRead(airQualitySenzorPin);
    airQuality = map(airQuality, 0, 1024, 0, 100);

    if (millis() - timeLastTransmitted >= transmitInterval) {
        printOverSerial(humd, temp, light, airQuality);
        movementDetected = false;
        timeLastTransmitted = millis();
    }         
}

void printOverSerial(int humd, int temp, int light, int airQuality)
{
    bt1.print("H:");
    bt1.print(humd);
    bt1.print("|L:");
    bt1.print(light);
    bt1.print("|T:");  
    bt1.print(temp);
    bt1.print("|Q:");     
    bt1.print(airQuality);
    bt1.print("|");
    Serial.print("Humid:");
    Serial.println(humd);
    Serial.print("Temp:");
    Serial.println(temp);  
    Serial.print("Light:");
    Serial.println(light);  
    Serial.print("AirQuality:");
    Serial.println(airQuality);      
    delay(50);
}
