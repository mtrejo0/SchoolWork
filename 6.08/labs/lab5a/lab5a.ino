#include <TFT_eSPI.h> // Graphics and font library for ST7735 driver chip
#include <SPI.h> //Used in support of TFT Display
#include <string.h>  //used for some string handling and processing.
 
 
TFT_eSPI tft = TFT_eSPI();  // Invoke library, pins defined in User_Setup.h
 
const int LOOP_PERIOD = 100; //periodicity of getting a number fact.
uint32_t last_time; //used for timing
 
void setup(){
  tft.init();
  tft.setRotation(2);
  tft.setTextSize(1);
  tft.fillScreen(TFT_BLACK);
  tft.setTextColor(TFT_GREEN, TFT_BLACK);
  Serial.begin(115200); //begin serial
  delay(100); //wait a bit (100 ms)
  last_time=millis();
 }
 
 
void loop(){
  tft.setCursor(5,0,2); //set cursor at top left of screen, and set font size to 1
  tft.println("I'm"); //print a whole line.
  tft.setCursor(5,20,2);
  tft.println("battery"); //print some text 
  tft.setCursor(5,40,2);
  tft.println("powered"); //continue printing from cursor
  tft.setCursor(5,60,2);
  tft.println(millis()); //print something that is changing so we can at least feel alive
  while (millis()-last_time < LOOP_PERIOD); //loop until LOOP_PERIOD has passed
  last_time = millis();
}       
