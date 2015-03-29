#include <VirtualWire.h>

const int transmit_pin = 12;
const int receive_pin = 11;
const int transmit_en_pin = 3;
const int relayPin = 6;

void setup()
{
    Serial.begin(9600);	
    pinMode(relayPin, OUTPUT);
    digitalWrite(relayPin, LOW); 
    Serial.println("start");
    vw_set_tx_pin(transmit_pin);
    vw_set_rx_pin(receive_pin);
    vw_set_ptt_pin(transmit_en_pin);
    vw_set_ptt_inverted(true); 
    vw_setup(2000);	
    vw_rx_start();    
    Serial.println("ititializing finished");
}

void loop()
{
    uint8_t buf[VW_MAX_MESSAGE_LEN];
    uint8_t buflen = VW_MAX_MESSAGE_LEN;
    if (vw_get_message(buf, &buflen))
    {
	Serial.print("Got: ");
	if(buf[0] == 'd') {
          openDoor();
        }
	Serial.println(buf[0]);
    }
}

void openDoor()
{
   digitalWrite(relayPin, HIGH); 
   delay(700);
   digitalWrite(relayPin, LOW); 
}
