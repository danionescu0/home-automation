#include <SoftwareSerial.h>

SoftwareSerial bt1(10, 11); // RX, TX

const int doorPin = 6;
long timeLastTransmitted;
boolean movementDetected = false;
const int pirSenzor = 2;
const long transmitInterval = 60000;

void setup()
{
    Serial.begin(9600);	
    bt1.begin(9600);    
    pinMode(doorPin, OUTPUT);
    digitalWrite(doorPin, LOW); 
    Serial.println("start");
}

void loop()
{
    if (bt1.available() > 0) {
        int received = bt1.read();
        Serial.println(received);    
        if (received == 'O') {
            Serial.println("Opening");
            openDoor();
        }  
    }
    int pir = getPirReading();
    if (millis() - timeLastTransmitted >= transmitInterval) {
        Serial.print("P:");Serial.print(pir);Serial.print("|");
        bt1.print("P:");bt1.print(pir);bt1.print("|");
        movementDetected = false;
        timeLastTransmitted = millis();       
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

