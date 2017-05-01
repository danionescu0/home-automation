// AESLib library: https://github.com/DavyLandman/AESLib
// RCSwitch library: https://github.com/sui77/rc-switch
// Livolo library will inside arduino-sketches folder

#include <AESLib.h>
#include <Livolo.h>
#include <RCSwitch.h>
#include <EncryptedSoftwareSerial.h>

const int transmitPin = 8;
const int lightsOffCode = 106;
const int lightsToggleCode = 120;
const char TERMINATOR = '|';
const int bufferSize = 19;
const String DEVICE_CODE = "L1"; // this will be used to identify incomming commands

Livolo livolo(transmitPin); // transmitter connected to pin #8
RCSwitch mySwitch = RCSwitch();
int switches[7] = {0, 6400, 6410, 6420, 6430, 6440, 6450};

uint8_t key[] = {48, 48, 48 , 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48};

EncryptedSoftwareSerial encryptedCommunicator = EncryptedSoftwareSerial(6,5, 9600, key, DEVICE_CODE);
int i;

void setup() 
{
    Serial.begin(9600);
    mySwitch.enableTransmit(transmitPin);
    Serial.println("init ok");
}

void loop() 
{
    if (encryptedCommunicator.parseIncomming()) {
        String command = encryptedCommunicator.getDecrypted();
        Serial.println(command);
        Serial.print("decripted:");Serial.println(command);
        computeSwitches(command);
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
    
    if (nr < 9) {
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


