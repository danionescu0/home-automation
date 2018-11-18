// BME680 library: https://github.com/adafruit/Adafruit_BME680.git
// Adafruit sensor library: https://github.com/adafruit/Adafruit_Sensor.git
// BH1750 library: https://github.com/claws/BH1750
// AESLib library: https://github.com/DavyLandman/AESLib
// Livolo library will inside arduino-sketches folder

#include <SoftwareSerial.h>
#include <Wire.h>
#include <SPI.h>
#include <Adafruit_Sensor.h>
#include "Adafruit_BME680.h"
#include <BH1750.h>
#include <Livolo.h>
#include <AESLib.h>
#include <EncryptedSoftwareSerial.h>

const int transmitPin = 8;
const int lightsOffCode = 106;
const int lightsToggleCode = 120;
const String DEVICE_CODE = "L1";
const long transmitInterval = 60000;


BH1750 lightMeter;
Adafruit_BME680 bme; // I2C
Livolo livolo(transmitPin); // transmitter connected to pin #8

uint8_t key[] = {48, 48, 48 , 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48};
long timeLastTransmitted;

EncryptedSoftwareSerial encryptedCommunicator = EncryptedSoftwareSerial(6, 5, 9600, key, DEVICE_CODE);

void setup() 
{
    Serial.begin(9600);
    Serial.print("Initializing..");
    if (!bme.begin()) {
      Serial.println("Could not find a valid BME680 sensor, check wiring!");
      while (1000);
    }    
    lightMeter.begin();
    bme.setTemperatureOversampling(BME680_OS_8X);
    bme.setHumidityOversampling(BME680_OS_2X);
    bme.setPressureOversampling(BME680_OS_4X);
    bme.setIIRFilterSize(BME680_FILTER_SIZE_3);
    bme.setGasHeater(320, 150); // 320*C for 150 ms    
    timeLastTransmitted = millis();
    for (int i=0;i<=10;i++) {
      bme.performReading();
    }

    Serial.println("Finish init");
}

void loop() 
{
    if (encryptedCommunicator.parseIncomming()) {
        String command = encryptedCommunicator.getDecrypted();
        Serial.print("Decripted:");Serial.println(command);
        computeSwitches(command);
    }
  
    if (millis() - timeLastTransmitted >= transmitInterval) {    
        bme.performReading();
        int humd = bme.humidity;
        int temp = bme.temperature;
        int light = lightMeter.readLightLevel();
        int airQuality = bme.gas_resistance / 1000.0;     
        transmitData(humd, temp, light, airQuality);
        timeLastTransmitted = millis();
    }         
}

void lightSwitch(int lightNr, boolean state)
{
    livolo.sendButton(lightNr, lightsOffCode);
    delay(500);    
    if (state) {    
        livolo.sendButton(lightNr, lightsToggleCode);
    }     
    delay(500);
}

void computeSwitches(String command)
{
    int nr = command.substring(0, command.length() - 1).toInt();
    boolean state = command.substring(command.length() - 1, command.length()) == "O" ? true : false;
    Serial.print("Nr:");Serial.println(nr);
    Serial.print("State:");Serial.println(state == true ? "TRUE" : "FALSE");
    lightSwitch(nr, state);
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
