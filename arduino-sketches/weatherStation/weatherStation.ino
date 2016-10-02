/*
 * This sketch uses: 
 * - BME280 sensor for pressure, temperature, and humidity
 * - a rain senzor
 * - a light senzor
 * It transmits data over serial using SoftwareSerial library, to be picked up by the HC-12 module 
 */
#include "LowPower.h"
#include <SoftwareSerial.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>

SoftwareSerial serialComm(4, 3); // RX, TX
Adafruit_BME280 bme; 

byte sensorsCode = 1;
const byte peripherialsPowerPin = 6;
char buffer[] = {' ',' ',' ',' ',' ',' ',' '};

struct sensorData
  {
      byte humidity;    
      byte temperature;
      byte rain;
      int  pressure;
      byte light;
  };

sensorData sensors;

void setup() 
{  
    Serial.begin(9600);
    serialComm.begin(9600);
    pinMode(peripherialsPowerPin, OUTPUT);
    digitalWrite(peripherialsPowerPin, HIGH);
    delay(500);
    if (!bme.begin()) {
        Serial.println("Could not find a valid BME280 sensor, check wiring!");
        while (1);
    }
    Serial.println("Initialization finished succesfully");
    delay(50);
    digitalWrite(peripherialsPowerPin, LOW);
}

void loop() 
{   
    deepSleep(7);    
    updateSenzors();
    transmitData();
}

void updateSenzors() 
{
    bme.begin();
    delay(100);
    sensors.temperature = bme.readTemperature();
    sensors.pressure = bme.readPressure() / 100.0F;
    sensors.humidity = bme.readHumidity();
}

void transmitData()
{
    emptyIncommingSerialBuffer();
    Serial.print("Temp:");Serial.println(sensors.temperature);
    Serial.print("Humid:");Serial.println(sensors.humidity);
    Serial.print("Pressure:");Serial.println(sensors.pressure);
    transmitSenzorData("T", sensors.temperature);
    transmitSenzorData("H", sensors.humidity);
    transmitSenzorData("PS", sensors.pressure);
}

void emptyIncommingSerialBuffer()
{
    while (serialComm.available() > 0) {
        serialComm.read();
        delay(5);
   }
}

void transmitSenzorData(String type, int value)
{
    serialComm.print(type);
    serialComm.print(sensorsCode);
    serialComm.print(":");
    serialComm.print(value);
    serialComm.print("|");
    delay(500);
}

void deepSleep(int eightSecondCycles)
{
    digitalWrite(peripherialsPowerPin, LOW);
    for (int i = 0; i < eightSecondCycles; i++) {
        LowPower.powerDown(SLEEP_8S, ADC_OFF, BOD_OFF);  
    }
    digitalWrite(peripherialsPowerPin, HIGH);
    delay(500);
}
