#include <SoftwareSerial.h>
#include <AESLib.h>
#include <EncryptedSoftwareSerial.h>



const byte pwmPower = 160;
const byte powerPwmPin = 9;
const byte relay1StatePin = 8;
const byte relay2StatePin = 7;
const String DEVICE_CODE = "L2";// this will be used to identify incomming commands
uint8_t key[] = {48, 48, 48 , 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48};


EncryptedSoftwareSerial encryptedCommunicator = EncryptedSoftwareSerial(10, 11, 9600, key, DEVICE_CODE);

void setup() 
{
    Serial.begin(9600);
    pinMode(powerPwmPin, OUTPUT);
    pinMode(relay1StatePin , OUTPUT);
    pinMode(relay2StatePin, OUTPUT);
    digitalWrite(powerPwmPin, LOW);
    digitalWrite(relay1StatePin, LOW);
    digitalWrite(relay2StatePin, LOW);  
    Serial.println("done init"); 
}

void loop() 
{
    if (encryptedCommunicator.parseIncomming()) {
        String command = encryptedCommunicator.getDecrypted();
        Serial.println(command);
        Serial.print("decripted:");Serial.println(command);
        toggleState(getState(command), getNumber(command));
    }
}

byte getNumber(String command)
{
    return command.substring(1, command.length()).toInt();
}

boolean getState(String command)
{
    String state = command.substring(0, 1);

    return state == "O" ? true : false;
}

void toggleState(boolean state, byte duration)
{  
    Serial.print("State:");Serial.println(state);
    Serial.print("Duration:");Serial.println(duration);
    if (state) {
        digitalWrite(relay1StatePin, HIGH);
        digitalWrite(relay2StatePin, HIGH);        
    } else {
        digitalWrite(relay1StatePin, LOW);
        digitalWrite(relay2StatePin, LOW);        
    }
    analogWrite(powerPwmPin, pwmPower);
    long millisecondsSleep = (long) duration * 1000;
    delay(millisecondsSleep);
    digitalWrite(powerPwmPin, LOW);
}

