#include "HX711.h"

//Scale stuff
HX711 scale;
uint8_t dataPin = 6;
uint8_t clockPin = 7;
uint32_t start, stop;
volatile float weight;

//Variables for reading commands over serial
char cmd;
int valve = 0;
int volume = 0;
bool exitReadVolume = false;

int valvePins[12] = {2, 3, 4, 5, 8, 9, 10, 11, 13, A0, A1, A2}; //pins that control the pinch valves that allow liquid to pass

long startPour = 0;
int timeout = 120000; //2 minute timeout. Failsafe so the valve isn't left open indefinitely.

void setup()
{
  Serial.begin(115200);  //Start serial connection for communication with main SBC

  scale.begin(dataPin, clockPin);   //Set up scale
  scale.set_scale(-100); //Calibration is handled on the SBC. -100 just makes the output positive and a reasonably sized number...

  for (int ii = 0; ii < 12; ii++) {  //Set up valve DO pins
    pinMode(valvePins[ii], OUTPUT);
    digitalWrite(valvePins[ii], LOW);
  }
}

void loop()
{
  if (Serial.available()) {
    if (Serial.read() == 80) { //80 = 'P' for pour
      //Parse serial input. Format is valve number (XX) and volume (YYY) as PXXYYY
      valve = (Serial.read()-48)*10 + Serial.read()-48; //This is an efficient way to pull out first two character integer since codepoint of 0 is 48
      volume = Serial.parseInt(); //parseInt() function converts remaining buffer into integer
      Serial.print("Valve number: ");
      Serial.println(valve);
      Serial.print("Volume (mL): ");
      Serial.println(volume);

      scale.tare(); //Tare the scale. Need to measure from zero even if there is already something in the cup

      digitalWrite(valvePins[valve], HIGH); //Open the valve specified in the command

      startPour = millis();
      weight = scale.get_units(5);
      while (weight < volume) { //Pour until the specified weight is reached (or timeout)
        weight = scale.get_units(5);
        Serial.print("Weight (oz/100): ");
        Serial.println(weight);

        if (millis() - startPour > timeout) { //Check how long the pour has been happening. Should timeout if cup tips over or something...
          Serial.println("TIMEOUT");
          break;
        }
      }

      digitalWrite(valvePins[valve], LOW); //Turn off valve, done pouring

      Serial.println();
      Serial.println("DONE"); //Tell the main SBC that pouring has completed

      Serial.flush(); //flush serial to be safe
    }
  }
  delay(250);
}
