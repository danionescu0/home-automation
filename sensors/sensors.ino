#include <VirtualWire.h>

const int transmit_pin = 12;
const int receive_pin = 11;
const int transmit_en_pin = 3;
const int airQualitySensorPin = 6;
byte msg[3];
byte reading;

void setup()
{
    Serial.begin(9600);	

    vw_set_tx_pin(transmit_pin);
    vw_set_rx_pin(receive_pin);
    vw_set_ptt_pin(transmit_en_pin);
    vw_set_ptt_inverted(true); 
    vw_setup(2000);  
}

void loop()
{
    reading = readAirQuality();
    sendData(15, reading);  
    delay(2000);
}


byte readAirQuality()
{
    int reading = analogRead(airQualitySensorPin);
    
    return map(reading, 0, 1023, 0, 100);
}

void sendData(byte senzorCode, byte senzorValue) 
{
    msg[0] = 's';
    msg[1] = senzorCode;
    msg[2] = senzorValue;
    vw_send(msg, 3);
    vw_wait_tx();   
    Serial.print("Sent:");
    Serial.println(senzorValue);  
}
