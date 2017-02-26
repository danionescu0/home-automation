// Simple blink example of Livolo.h library for Livolo wireless light switches

#include <livolo.h>

Livolo livolo(8); // transmitter connected to pin #8


void setup() {
}

void loop() {
 
  livolo.sendButton(6400, 120); // blink button #3 every 3 seconds using remote with remoteID #6400
  delay(3000);
  
}
