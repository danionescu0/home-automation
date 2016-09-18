/*
 * This sketch uses: 
 * - BME280 sensor for pressure, temperature, and humidity
 * - a rain senzor
 * - a light senzor
 * It transmits data over serial using SoftwareSerial library, to be picked up by the HC-12 module 
 */

#include <SoftwareSerial.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>

SoftwareSerial serialComm(6, 5); // RX, TX
Adafruit_BME280 bme; 

long timeLastTransmitted;
byte sensorsCode = 1;
const long transmitInterval = 60000;
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
    serialComm.begin(9600);
    Serial.begin(9600);
      if (!bme.begin()) {
          Serial.println("Could not find a valid BME280 sensor, check wiring!");
      while (1);
    }
    Serial.println("Initialization finished succesfully");
}

void loop() 
{
    if (millis() - timeLastTransmitted >= transmitInterval) {      
        //airQuality = map(airQuality, 0, 1024, 0, 100);      
        updateSenzors();
        transmitData();
        timeLastTransmitted = millis();
    }         
}

void updateSenzors() 
{
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
    delay(100);    
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
}
