/*
 * External libraries:
 *       EnergyMonitor library: https://github.com/openenergymonitor/EmonLib
 *       
 * Commands an electromagnetic lock (using pin 6)
 * Periodically polls a PIR senzor and transmit data
 * Using the Emon lib calculate power consumption and transmits it
 * 
 * The communication is done via external serial (using Software serial), it can be a HC-05, HC-12 or 
 * other wireless device that communicates through serial with the arduino
*/
#include <SoftwareSerial.h>
#include "EmonLib.h" 

SoftwareSerial serialComm(10, 11); // RX, TX
EnergyMonitor emon; 

const int doorPin = 6;
const int pirSenzor = 2;
const long transmitInterval = 60000;
const int voltage = 230;
const double emonCalibrationValue = 60.6;

long timeLastTransmitted;
boolean movementDetected = false;
double sumOfReadings = 0;
int nrOfReadings = 0;


void setup()
{
    Serial.begin(9600);	
    serialComm.begin(9600);    
    pinMode(doorPin, OUTPUT);
    digitalWrite(doorPin, LOW); 
    emon.current(1, emonCalibrationValue);
    Serial.println("start");
}

void loop()
{
    if (serialComm.available() > 0) {
        int received = serialComm.read();
        Serial.println(received);    
        if (received == 'O') {
            Serial.println("Opening");
            openDoor();
        }  
    }
    int pir = getPirReading();
    readPower();
    if (millis() - timeLastTransmitted >= transmitInterval) {
        transmitSenzorData("P", pir);
        transmitSenzorData("W", getPowerAverage());
        resetMovementDetector();
        resetPowerReading();
    }
}

void openDoor()
{
   digitalWrite(doorPin, HIGH); 
   delay(500);
   digitalWrite(doorPin, LOW); 
}

int getPirReading()
{
    if (movementDetected) {
        return true;
    }    
    movementDetected = digitalRead(pirSenzor);
    
    return movementDetected;
}

void readPower()
{
    sumOfReadings += emon.calcIrms(1480);
    nrOfReadings ++;    
}

int getPowerAverage()
{
    return (sumOfReadings / nrOfReadings) * voltage;
}

void resetPowerReading()
{
    sumOfReadings = 0;
    nrOfReadings = 0;
}

void resetMovementDetector()
{
    movementDetected = false;
    timeLastTransmitted = millis();    
}

void transmitSenzorData(String sensorsCode, int value)
{
    Serial.print(sensorsCode);
    Serial.print(":");
    Serial.print(value);
    Serial.print("|");
    serialComm.print(sensorsCode);
    serialComm.print(":");
    serialComm.print(value);
    serialComm.print("|");
    delay(10);
}

