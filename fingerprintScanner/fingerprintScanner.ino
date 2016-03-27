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
}

void loop()
{
	if (fps.IsPressFinger())
	{
  		fps.CaptureFinger(false);
  		int id = fps.Identify1_N();
  		if (id == 0 || id == 1)
  		{
  			  Serial.print("Verified ID:");
  			  Serial.println(id);
          bluetooth.write("F:");
          char buffer[1];
          dtostrf(id, 1, 0, buffer);
          bluetooth.write(buffer);
          bluetooth.write("|");
          delay(1000);
  		} else {
  			Serial.println("Finger not found");
  		}
  	  delay(100);
  }
}
