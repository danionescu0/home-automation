/*
  Morse.h - Library for Livolo wireless switches.
  Created by Sergey Chernov, October 25, 2013.
  Released into the public domain.
*/

#ifndef Livolo_h
#define Livolo_h

#include "Arduino.h"

class Livolo
{
  public:
    Livolo(byte pin);
    void sendButton(unsigned int remoteID, byte keycode);
  private:
    byte txPin;
	byte i; // just a counter
	byte pulse; // counter for command repeat
	boolean high; // pulse "sign"
	void selectPulse(byte inBit);
	void sendPulse(byte txPulse);
};

#endif