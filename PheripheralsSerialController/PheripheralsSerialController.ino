#include <Livolo.h>
#include <RCSwitch.h>

Livolo livolo(8); // transmitter connected to pin #8
RCSwitch mySwitch = RCSwitch();

const int lightsOffCode = 106;
const int lightsToggleCode = 120;
char *controller;
char buffer[] = {' ',' ',' ',' ',' ',' ',' '};

int switches[5] =
          {
            0, 6400, 6410, 6420, 6430
          };
void setup() 
{
    Serial.begin(9600);
    Serial.setTimeout(200);
    mySwitch.enableTransmit(8);
}

void loop() 
{
    if (Serial.available()) {
      while (!Serial.available()); // Wait for characters
      Serial.readBytesUntil('|', buffer, 7);  
      Serial.write((int) buffer[0]);
      if (buffer[0] <= 57 && buffer[0] >= 56) {
          //power sockets begining with digit 8 ending with 9
          powerSocket(buffer);
      } else if (buffer[0] <= 52 && buffer[0] >= 49) {
          // light switch beinging with digit 1 ending with 4
          lightSwitch(buffer);
      }
      delay(10);  
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

void printBuf(uint8_t *buf) 
{
    for (byte i = 0; i < 3; i++) {
        Serial.print(buf[i]);
        Serial.print(",");
    }
    Serial.println();
    delay(30);
}
