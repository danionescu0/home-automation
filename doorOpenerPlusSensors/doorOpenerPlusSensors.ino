#include <SoftwareSerial.h>

SoftwareSerial bt1(10, 11); // RX, TX
const int relayPin = 6;

void setup()
{
    Serial.begin(9600);	
    bt1.begin(9600);    
    pinMode(relayPin, OUTPUT);
    digitalWrite(relayPin, LOW); 
    Serial.println("start");
    Serial.println("ititializing finished");
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
}

void openDoor()
{
   digitalWrite(relayPin, HIGH); 
   delay(700);
   digitalWrite(relayPin, LOW); 
}
