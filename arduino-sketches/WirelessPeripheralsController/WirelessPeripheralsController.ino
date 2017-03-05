// AESLib library: https://github.com/DavyLandman/AESLib
// RCSwitch library: https://github.com/sui77/rc-switch
// Livolo library will inside arduino-sketches folder

#include <SoftwareSerial.h>
#include <AESLib.h>
#include <Livolo.h>
#include <RCSwitch.h>

const int transmitPin = 8;
const int lightsOffCode = 106;
const int lightsToggleCode = 120;
const char TERMINATOR = '|';
const int bufferSize = 19;
const String DEVICE_CODE = "XX"; // this will be used to identify incomming commands

SoftwareSerial serialWirelessDevice(10, 11); // RX, TX
Livolo livolo(transmitPin); // transmitter connected to pin #8
RCSwitch mySwitch = RCSwitch();
int switches[7] = {0, 6400, 6410, 6420, 6430, 6440, 6450};
char buffer[19];

uint8_t key[] = {48, 48, 48 , 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48};
char data[16];

int i;

void setup() 
{
    Serial.begin(9600);
    serialWirelessDevice.begin(9600);
    serialWirelessDevice.setTimeout(100);
    mySwitch.enableTransmit(transmitPin);
    for (i=0;i<=bufferSize - 1; i++){
        buffer[i] = ' ';
    }
    char data[] = "                ";
}

void loop() 
{
    if (serialWirelessDevice.available() > 0) {   
        serialWirelessDevice.readBytes(buffer, 19);
        if (isForThisDevice()) {        
            String command = decrypt();
            Serial.print("decripted:");Serial.println(command);
            computeSwitches(command);
        }
        clearBuffer();  
    } 
}

boolean isForThisDevice()
{
    String incommingDeviceCode = "";
    incommingDeviceCode += buffer[0];
    incommingDeviceCode += buffer[1];

    return incommingDeviceCode == DEVICE_CODE;
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

String decrypt()
{
    for (i=0;i<=15;i++) {
        data[i] = buffer[i+3];
    }
    aes128_cbc_dec(key, key, data, 16);
    String result = "";
    for (i=0;i<=15;i++) {
        if (data[i] == TERMINATOR) {
            return result;
        }
        result += data[i];
    }

    return result;
}

void clearBuffer()
{
    for (int i=0; i<=bufferSize - 1; i++) {
        buffer[i] = ' ';
    }
}

