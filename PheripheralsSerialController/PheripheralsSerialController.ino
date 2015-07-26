#include <Livolo.h>
#include <VirtualWire.h>

Livolo livolo(8); // transmitter connected to pin #8
const int transmit_pin = 12;
const int receive_pin = 11;
const int transmit_en_pin = 3;
char *controller;

void setup() 
{
    Serial.begin(9600);
    vw_set_tx_pin(transmit_pin);
    vw_set_rx_pin(receive_pin);
    vw_set_ptt_pin(transmit_en_pin);
    vw_set_ptt_inverted(true); 
    vw_setup(2000);	
    //vw_rx_start();   
}

void loop() 
{
    if (Serial.available()) {
      char received = Serial.read();
      //Serial.write(received);
      if (received == '1') {
        //vw_rx_stop(); 
        livolo.sendButton(6400, 120);
        //vw_rx_start(); 
        Serial.println("toggle1");
      } else if (received == '2') {
        //vw_rx_stop(); 
        livolo.sendButton(6410, 120);
        //vw_rx_start(); 
        Serial.println("toggle2");
      } else if (received == '3') {
        Serial.println("Sending open door");
        controller = "d"  ;
        //vw_rx_stop(); 
        vw_send((uint8_t *)controller, strlen(controller));
        vw_wait_tx();  
        //vw_rx_start();    
      } 
      delay(10);  
    }
    uint8_t buf[VW_MAX_MESSAGE_LEN];
    uint8_t buflen = VW_MAX_MESSAGE_LEN;
    if (vw_get_message(buf, &buflen))
    {
	if(buf[0] == 's') {
            printBuf(buf);
        }
    }  
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
