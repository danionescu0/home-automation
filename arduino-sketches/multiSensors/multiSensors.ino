// HTU21D library: https://github.com/adafruit/Adafruit_HTU21DF_Library
// BH1750 library: https://github.com/claws/BH1750
// RCSwitch library: https://github.com/sui77/rc-switch
// Livolo library will inside arduino-sketches folder

#include <SoftwareSerial.h>
#include <Wire.h>
#include "HTU21D.h"
#include <BH1750.h>
#include <Livolo.h>
#include <RCSwitch.h>

SoftwareSerial bt1(6, 5); // RX, TX
HTU21D tempHumid;
BH1750 lightMeter;
const int transmitPin = 8;
Livolo livolo(transmitPin); // transmitter connected to pin #8
RCSwitch mySwitch = RCSwitch();

const int airQualitySenzorPin = A3;
long timeLastTransmitted;
boolean movementDetected = false;
const long transmitInterval = 60000;


const int lightsOffCode = 106;
const int lightsToggleCode = 120;
char buffer[] = {' ',' ',' ',' ',' ',' ',' '};

int switches[7] =
          {
            0, 6400, 6410, 6420, 6430, 6440, 6450
          };

void setup() 
{
  bt1.begin(9600);
  Serial.begin(9600);
  tempHumid.begin();
  lightMeter.begin();
  timeLastTransmitted = millis();
  mySwitch.enableTransmit(transmitPin);
  Serial.println("Finish init");
}

void loop() 
{
    if (bt1.available()) {
        Serial.println("smth");
        while (!bt1.available()); // Wait for characters
        bt1.readBytesUntil('|', buffer, 7);  
        Serial.write((int) buffer[0]);
        if (buffer[0] <= 57 && buffer[0] >= 56) {
            //power sockets begining with digit 8 ending with 9
            powerSocket(buffer);
        } else if (buffer[0] <= 54 && buffer[0] >= 49) {
            // light switch beinging with digit 1 ending with 6
            lightSwitch(buffer);
        }
        delay(10);  
    }

    if (millis() - timeLastTransmitted >= transmitInterval) {      
        int humd = tempHumid.readHumidity();
        int temp = tempHumid.readTemperature();
        int light = lightMeter.readLightLevel();
        int airQuality = analogRead(airQualitySenzorPin);
        airQuality = map(airQuality, 0, 1024, 0, 100);      
        printOverSerial(humd, temp, light, airQuality);
        movementDetected = false;
        timeLastTransmitted = millis();
    }         
}

void powerSocket(char buffer[]) 
{
    Serial.println("Computing power socker, and anything with rc switch lib");
    switch (buffer[0]) {
        case '8':
            if (buffer[1] == 'O') {
                mySwitch.send(1381717, 24);      
            } else {
                mySwitch.send(1381716, 24);
            }
            break;
        case '9':
            if (buffer[1] == 'O') {
                mySwitch.send(1397845, 24);      
            } else {
                mySwitch.send(1397844, 24);
            }
            break;            
    }
}

void lightSwitch(char buffer[])
{
    Serial.println("computing light switch");
    String convert;
    convert = convert + buffer[0];
    int remoteId = convert.toInt();
    int remoteCode = switches[remoteId];
    int sendCode = lightsToggleCode;
    livolo.sendButton(remoteCode, lightsOffCode);
    Serial.println("Sending close");
    delay(500);    
    if (buffer[1] == 'O') {
      Serial.println("Sending open");      
        livolo.sendButton(remoteCode, lightsToggleCode);
    }     
    delay(100);
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
