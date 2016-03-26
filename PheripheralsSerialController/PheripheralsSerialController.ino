#include <Livolo.h>
#include <RCSwitch.h>
#include <SoftwareSerial.h>

Livolo livolo(8); // transmitter connected to pin #8
RCSwitch mySwitch = RCSwitch();
SoftwareSerial mySerial(9, 10); // RX, TX

const int transmitterPowerPin = 7;
const int rcSwitchPin = 8;
const int lightsOffCode = 106;
const int lightsToggleCode = 120;
char *controller;
char buffer[] = {' ',' ',' ',' ',' ',' ',' '};

int switches[7] =
          {
            0, 6400, 6410, 6420, 6430, 6440, 6450
          };
          
void setup() 
{
    Serial.begin(9600);
    mySerial.begin(9600);
    mySerial.setTimeout(70);    
    mySwitch.enableTransmit(rcSwitchPin);
    pinMode(transmitterPowerPin, OUTPUT);
    digitalWrite(transmitterPowerPin, HIGH);
    Serial.println("Init done");
}

void loop() 
{
    if (mySerial.available()) {
      while (!mySerial.available()); // Wait for characters
      mySerial.readBytesUntil('|', buffer, 7);  
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
}

void powerSocket(char buffer[]) 
{
    Serial.println("Computing power socker, and anything with rc switch lib");
    //digitalWrite(transmitterPowerPin, HIGH);
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
    //digitalWrite(transmitterPowerPin, LOW);
}

void lightSwitch(char buffer[])
{
    //digitalWrite(transmitterPowerPin, HIGH);
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
    //digitalWrite(transmitterPowerPin, LOW);
}
