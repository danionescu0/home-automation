#include <JeeLib.h>
#include <VirtualWire.h>

const int transmit_pin = 12;
const int receive_pin = 2;
const int transmit_en_pin = 3;
int ledBeacon = 5;
int sensor = A0;

ISR(WDT_vect) { Sleepy::watchdogEvent(); } // Setup the watchdog
 
void setup() 
{
    Serial.begin(9600);
    pinMode(ledBeacon, OUTPUT);
    vw_set_tx_pin(transmit_pin);
    vw_set_rx_pin(receive_pin);
    vw_set_ptt_pin(transmit_en_pin);
    vw_set_ptt_inverted(true); // Required for DR3100
    vw_setup(2000);	 // Bits per sec   
}
 
void loop() 
{ 
   digitalWrite(ledBeacon, HIGH);
   delay(100);
   if (analogRead(sensor) > 90) { //mailbox empty
       Serial.println("empty");
       transmit(false);
   } else {
       Serial.println("full");     
       transmit(true);
   }
   delay(10);
   digitalWrite(ledBeacon, LOW);   

   
   Sleepy::loseSomeTime(5000);
}

void transmit(boolean status)
{
  char s;
  if (status) {
      s = 'F';
  } else {
      s = 'E';
  }
  char msg[1] = {s};  
  vw_send((uint8_t *)msg, 1);
  vw_wait_tx(); // Wait until the whole message is gone  
}
