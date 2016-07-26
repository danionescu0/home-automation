#include "FPS_GT511C3.h"
#include "SoftwareSerial.h"

FPS_GT511C3 fps(4, 5);
SoftwareSerial bluetooth(7, 8); // RX, TX

void setup()
{
  	Serial.begin(9600);
    bluetooth.begin(9600);
  	delay(100);
  	fps.Open();
  	fps.SetLED(true);
    Serial.println("ok");
}

void loop()
{
  	if (fps.IsPressFinger()) {
        int id = getFingerId();
        if (isKnownFinger(id)) {
      		  Serial.print("Verified ID:");
      		  Serial.println(id);
            sendFingerId(id);
            signalKnownFinger();
            delay(1000);
    		} else {
            signalUnknownFinger();
    		}
  	}
    delay(100);
}

bool isKnownFinger(int id)
{   
    return (id == 0 || id == 1);
}

int getFingerId()
{
    fps.CaptureFinger(false);
    int id = fps.Identify1_N();
    
    return id;
}

void sendFingerId(int id)
{
    bluetooth.write("F:");
    char buffer[1];
    dtostrf(id, 1, 0, buffer);
    bluetooth.write(buffer);
    bluetooth.write("|");  
}

void signalKnownFinger()
{
    fps.SetLED(false);  
    delay(500);
    fps.SetLED(true);
}

void signalUnknownFinger()
{
    for (int i=0;i<= 2; i++) {
        fps.SetLED(false);  
        delay(300);
        fps.SetLED(true); 
    } 
}

