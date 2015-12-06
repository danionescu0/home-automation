#include <Livolo.h>
#include <VirtualWire.h>

Livolo livolo(8); // transmitter connected to pin #8
const int transmit_pin = 12;
const int receive_pin = 11;
const int transmit_en_pin = 3;
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
    vw_set_tx_pin(transmit_pin);
    vw_set_rx_pin(receive_pin);
    vw_set_ptt_pin(transmit_en_pin);
    vw_set_ptt_inverted(true); 
    vw_setup(2000);  
}

void loop() 
{
    if (Serial.available()) {
      while (!Serial.available()); // Wait for characters
      Serial.readBytesUntil('!', buffer, 7);  
      Serial.write((int) buffer[0]);
      if (buffer[0] == '0') {
          Serial.println("Sending open door");
          controller = "d";
          vw_send((uint8_t *)controller, strlen(controller));
          vw_wait_tx();          
      } else if (buffer[0] <= 52 && buffer[0] >= 49) {
          lightSwitch(buffer);
      }
      delay(10);  
    }
    uint8_t buf[VW_MAX_MESSAGE_LEN];
    uint8_t buflen = VW_MAX_MESSAGE_LEN;
    if (vw_get_message(buf, &buflen)) {
  	  if(buf[0] == 's') {
              printBuf(buf);
          }
    }  
}

void lightSwitch(char buffer[])
{
    Serial.println("computing");
    String convert;
    convert = convert + buffer[0];
    int remoteId = convert.toInt();
    int remoteCode = switches[remoteId];
    int sendCode = lightsToggleCode;
    livolo.sendButton(remoteCode, lightsOffCode);
    delay(500);    
    if (buffer[1] == 'O') {
        livolo.sendButton(remoteCode, lightsToggleCode);
    }    
    //Serial.println(remoteCode);    
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
