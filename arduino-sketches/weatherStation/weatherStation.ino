/*
 * This sketch uses: 
 * - BME280 sensor for pressure, temperature, and humidity
 * - a light senzor
 * It transmits data over serial using SoftwareSerial library, to be picked up by the HC-12 module
 * BH1750 library: https://github.com/claws/BH1750
 * LowPower library: https://github.com/rocketscream/Low-Power
 * Adafruit Sensor library: https://github.com/adafruit/Adafruit_Sensor
 * Adafruit BME280 library: https://github.com/adafruit/Adafruit_BME280_Library
 */
#include "LowPower.h"
#include "SoftwareSerial.h"
#include "Wire.h"
#include "Adafruit_Sensor.h"
#include "Adafruit_BME280.h"
#include "BH1750.h"

SoftwareSerial serialComm(4, 5); // RX, TX
Adafruit_BME280 bme; 
BH1750 lightMeter;
const byte rainPin = A0;

byte sensorsCode = 1;
/**
 * voltage level that will pun the microcontroller in deep sleep instead of regular sleep
 */
int voltageDeepSleepThreshold = 4200; 
const byte peripherialsPowerPin = 6;
char buffer[] = {' ',' ',' ',' ',' ',' ',' '};


struct sensorData
  {
      byte humidity;    
      int temperature;
      byte rain;
      int  pressure;
      long voltage;
      int light;
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
        while (1) {
           customSleep(100);
        }
    }
    Serial.println("Initialization finished succesfully");
    delay(50);
    digitalWrite(peripherialsPowerPin, HIGH);
}

void loop() 
{    
    updateSenzors();
    transmitData();    
    customSleep(75);       
}

void updateSenzors() 
{
    bme.begin();
    lightMeter.begin();
    delay(300);
    sensors.temperature = bme.readTemperature();
    sensors.pressure = bme.readPressure() / 100.0F;
    sensors.humidity = bme.readHumidity();
    sensors.light = lightMeter.readLightLevel();
    sensors.voltage = readVcc();
    sensors.rain = readRain();
}

void transmitData()
{
    emptyIncommingSerialBuffer();
    Serial.print("Temp:");Serial.println(sensors.temperature);
    Serial.print("Humid:");Serial.println(sensors.humidity);
    Serial.print("Pressure:");Serial.println(sensors.pressure);
    Serial.print("Light:");Serial.println(sensors.light);
    Serial.print("Voltage:");Serial.println(sensors.voltage);
    Serial.print("Rain:");Serial.println(sensors.rain);
    transmitSenzorData("T", sensors.temperature);
    transmitSenzorData("H", sensors.humidity);
    transmitSenzorData("PS", sensors.pressure);
    transmitSenzorData("L", sensors.light);
    transmitSenzorData("V", sensors.voltage);
    transmitSenzorData("R", sensors.rain);
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
    delay(50);
}

void customSleep(long eightSecondCycles)
{
    if (sensors.voltage > voltageDeepSleepThreshold) {
        delay(eightSecondCycles * 8000);
        return;
    }
    digitalWrite(peripherialsPowerPin, LOW);
    for (int i = 0; i < eightSecondCycles; i++) {
        LowPower.powerDown(SLEEP_8S, ADC_OFF, BOD_OFF);  
    }
    digitalWrite(peripherialsPowerPin, HIGH);
    delay(500);
}

byte readRain()
{
    byte level = analogRead(rainPin);

    return map(level, 0, 1023, 0, 100);  
}

long readVcc() {
    // Read 1.1V reference against AVcc
    // set the reference to Vcc and the measurement to the internal 1.1V reference
    #if defined(__AVR_ATmega32U4__) || defined(__AVR_ATmega1280__) || defined(__AVR_ATmega2560__)
      ADMUX = _BV(REFS0) | _BV(MUX4) | _BV(MUX3) | _BV(MUX2) | _BV(MUX1);
    #elif defined (__AVR_ATtiny24__) || defined(__AVR_ATtiny44__) || defined(__AVR_ATtiny84__)
      ADMUX = _BV(MUX5) | _BV(MUX0);
    #elif defined (__AVR_ATtiny25__) || defined(__AVR_ATtiny45__) || defined(__AVR_ATtiny85__)
      ADMUX = _BV(MUX3) | _BV(MUX2);
    #else
      ADMUX = _BV(REFS0) | _BV(MUX3) | _BV(MUX2) | _BV(MUX1);
    #endif  
  
    delay(2); // Wait for Vref to settle
    ADCSRA |= _BV(ADSC); // Start conversion
    while (bit_is_set(ADCSRA,ADSC)); // measuring
    uint8_t low  = ADCL; // must read ADCL first - it then locks ADCH  
    uint8_t high = ADCH; // unlocks both
    long result = (high<<8) | low;
    result = 1125300L / result; // Calculate Vcc (in mV); 1125300 = 1.1*1023*1000
    
    return result; // Vcc in millivolts
}
