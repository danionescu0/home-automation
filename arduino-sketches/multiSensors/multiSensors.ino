// HTU21D library: https://github.com/adafruit/Adafruit_HTU21DF_Library
// BH1750 library: https://github.com/claws/BH1750
// RCSwitch library: https://github.com/sui77/rc-switch
// AESLib library: https://github.com/DavyLandman/AESLib
// Livolo library will inside arduino-sketches folder

#include <SoftwareSerial.h>
#include <Wire.h>
#include "HTU21D.h"
#include <BH1750.h>
#include <Livolo.h>
#include <RCSwitch.h>
#include <AESLib.h>
#include <EncryptedSoftwareSerial.h>

const int transmitPin = 8;
const int lightsOffCode = 106;
const int lightsToggleCode = 120;
const String DEVICE_CODE = "L1";// this will be used to identify incomming commands
const long transmitInterval = 60000;
const int airQualitySenzorPin = A3;

HTU21D tempHumid;
BH1750 lightMeter;
Livolo livolo(transmitPin); // transmitter connected to pin #8
RCSwitch mySwitch = RCSwitch();
int switches[7] = {0, 6400, 6410, 6420, 6430, 6440, 6450};
uint8_t key[] = {48, 48, 48 , 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48};
int i;
long timeLastTransmitted;
boolean movementDetected = false;

EncryptedSoftwareSerial encryptedCommunicator = EncryptedSoftwareSerial(6, 5, 9600, key, DEVICE_CODE);

void setup() 
{
    Serial.begin(9600);
    tempHumid.begin();
    lightMeter.begin();
    timeLastTransmitted = millis();
    mySwitch.enableTransmit(transmitPin);
    Serial.println("Finish init");
}

void loop() 
{
    if (encryptedCommunicator.parseIncomming()) {
        String command = encryptedCommunicator.getDecrypted();
        Serial.println(command);
        Serial.print("decripted:");Serial.println(command);
        computeSwitches(command);
    }

    if (millis() - timeLastTransmitted >= transmitInterval) {      
        int humd = tempHumid.readHumidity();
        int temp = tempHumid.readTemperature();
        int light = lightMeter.readLightLevel();
        int airQuality = analogRead(airQualitySenzorPin);
        airQuality = map(airQuality, 0, 1024, 0, 100);      
        transmitData(humd, temp, light, airQuality);
        movementDetected = false;
        timeLastTransmitted = millis();
    }         
}

void powerSocket(byte switchNr, boolean state) 
{
    switch (switchNr) {
        case 8:
            if (state) {
                mySwitch.send(1381717, 24);      
            } else {
                mySwitch.send(1381716, 24);
            }
            break;
        case 9:
            if (state) {
                mySwitch.send(1397845, 24);      
            } else {
                mySwitch.send(1397844, 24);
            }
            break;            
    }
}

void lightSwitch(byte lightNr, boolean state)
{
    int remoteCode = switches[lightNr];
    int sendCode = lightsToggleCode;
    livolo.sendButton(remoteCode, lightsOffCode);
    delay(500);    
    if (state) {    
        livolo.sendButton(remoteCode, lightsToggleCode);
    }     
    delay(100);
}

void computeSwitches(String command)
{
    byte nr = getNumber(command);
    boolean state = getState(command);
    Serial.print("nr:");Serial.println(nr);
    if (state) {
      Serial.print("state:");Serial.println("TRUE");
    } else {
      Serial.print("state:");Serial.println("FALSE");
    }
    
    if (nr < 8) {
        lightSwitch(nr, state);
    } else {
        powerSocket(nr, state);
    }
}

byte getNumber(String command)
{
    return command.substring(0, command.length() - 1).toInt();
}

boolean getState(String command)
{
    String state = command.substring(command.length() - 1, command.length());

    return state == "O" ? true : false;
}


void transmitData(int humd, int temp, int light, int airQuality)
{
    encryptedCommunicator.transmit("H:");encryptedCommunicator.transmit(String(humd));
    encryptedCommunicator.transmit("|L:");encryptedCommunicator.transmit(String(light));
    encryptedCommunicator.transmit("|T:");encryptedCommunicator.transmit(String(temp));
    encryptedCommunicator.transmit("|Q:");encryptedCommunicator.transmit(String(airQuality));
    encryptedCommunicator.transmit("|");
    Serial.print("Humid:");Serial.println(humd);
    Serial.print("Temp:");Serial.println(temp);  
    Serial.print("Light:");Serial.println(light);  
    Serial.print("AirQuality:");Serial.println(airQuality);      
    delay(50);
}
