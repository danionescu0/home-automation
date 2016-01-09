#include <SoftwareSerial.h>
#include <Wire.h>
#include "HTU21D.h"
#include <BH1750.h>

SoftwareSerial bt1(6, 5); // RX, TX
HTU21D tempHumid;
BH1750 lightMeter;

long timeLastTransmitted;
boolean movementDetected = false;
const int pirSenzor = 2;
const long transmitInterval = 60000;

void setup() 
{
  bt1.begin(9600);
  Serial.begin(9600);
  tempHumid.begin();
  lightMeter.begin();
  pinMode(pirSenzor, INPUT);  
  timeLastTransmitted = millis();
}

void loop() 
{
    int humd = tempHumid.readHumidity();
    int temp = tempHumid.readTemperature();
    int light = lightMeter.readLightLevel();
    int pir = getPirReading();

    if (millis() - timeLastTransmitted >= transmitInterval) {
        printOverSerial(humd, temp, light, (int) pir);
        movementDetected = false;
        timeLastTransmitted = millis();
    }         
}

int getPirReading()
{
    if (movementDetected) {
        return true;
    }    
    movementDetected = digitalRead(pirSenzor);
    
    return movementDetected;
}

void printOverSerial(int humd, int temp, int light, int pir)
{
    bt1.print("H:");
    bt1.print(humd);
    bt1.print("|L:");
    bt1.print(light);
    bt1.print("|T:");  
    bt1.print(temp);
    bt1.print("|P:");  
    bt1.print(pir);
    bt1.print("|");  
    Serial.print("Pir:");
    Serial.println(pir);    
    Serial.print("Humid:");
    Serial.println(humd);
    Serial.print("Temp:");
    Serial.println(temp);  
    Serial.print("Light:");
    Serial.println(light);  
    delay(50);
}
