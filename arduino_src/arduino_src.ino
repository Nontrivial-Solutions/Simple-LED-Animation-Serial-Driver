/*
  Serial Event example

  When new serial data arrives, this sketch adds it to a String.
  When a newline is received, the loop prints the string and clears it.

  A good test for this is to try it with a GPS receiver that sends out
  NMEA 0183 sentences.

  NOTE: The serialEvent() feature is not available on the Leonardo, Micro, or
  other ATmega32U4 based boards.

  created 9 May 2011
  by Tom Igoe

  This example code is in the public domain.

  http://www.arduino.cc/en/Tutorial/SerialEvent
*/

#include "FastLED.h"
#define NUM_LEDS 1680
#define DATA_PIN 6

CRGB leds[NUM_LEDS];

String inputString = "";         // a String to hold incoming data
bool stringComplete = false;  // whether the string is complete

void setup() {
  // initialize serial:
  Serial.begin(115200);
  // reserve 200 bytes for the inputString:
  inputString.reserve(200);

  // setup LED array
  FastLED.addLeds<NEOPIXEL, DATA_PIN>(leds, NUM_LEDS);
}

void loop() {
  // print the string when a newline arrives:
  if (stringComplete) {

    String LEDdec = getValue(inputString, ' ', 0);
    String LEDval = getValue(inputString, ' ', 1);
    int LEDvalInt = LEDval.toInt();
    String RGBdec = getValue(inputString, ' ', 2);
    String Rval = getValue(inputString, ' ', 3);
    String Gval = getValue(inputString, ' ', 4);
    String Bval = getValue(inputString, ' ', 5);
    
    int RvalInt = Rval.toInt();
    int GvalInt = Gval.toInt();
    int BvalInt = Bval.toInt();

    //Serial.println(LEDdec);
    //Serial.println(LEDval);
    //Serial.println(RGBdec);
    //Serial.println(Rval);
    //Serial.println(Gval);
    //Serial.println(Bval);

    leds[LEDvalInt].r = RvalInt;
    leds[LEDvalInt].g = GvalInt;
    leds[LEDvalInt].b = BvalInt;
    FastLED.show();
    delay(30);

    // clear the string:
    inputString = "";
    stringComplete = false;
  }
}

/*
  SerialEvent occurs whenever a new data comes in the hardware serial RX. This
  routine is run between each time loop() runs, so using delay inside loop can
  delay response. Multiple bytes of data may be available.
*/
void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the inputString:
    inputString += inChar;
    // if the incoming character is a newline, set a flag so the main loop can
    // do something about it:
    if (inChar == '\n') {
      stringComplete = true;
    }
  }
}

String getValue(String data, char separator, int index)
{
  int found = 0;
  int strIndex[] = { 0, -1 };
  int maxIndex = data.length() - 1;

  for (int i = 0; i <= maxIndex && found <= index; i++) {
    if (data.charAt(i) == separator || i == maxIndex) {
      found++;
      strIndex[0] = strIndex[1] + 1;
      strIndex[1] = (i == maxIndex) ? i + 1 : i;
    }
  }
  return found > index ? data.substring(strIndex[0], strIndex[1]) : "";
}
