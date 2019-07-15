#include <SPI.h>
#include <TFT_eSPI.h>
TFT_eSPI tft = TFT_eSPI();


#define BLACK 0
#define C1 1
#define C2 2
#define COLOR 3
#define B1 4
#define B2 5


const int UPDATE_PERIOD = 20;
const uint8_t PIN_1 = 16; //button 1
const uint8_t PIN_2 = 5; //button 2
uint32_t primary_timer;
float sample_rate = 2000; //Hz
float sample_period = (int)(1e6 / sample_rate);
int change = 0;
float thesh = 1;

const uint8_t BAR_WIDTH = 30;
const uint8_t BAR_X = 50;
const uint8_t SCREEN_YMAX = 159;
int render_counter;
uint16_t raw_reading;
uint16_t scaled_reading_for_lcd;
uint16_t old_scaled_reading_for_lcd;
float scaled_reading_for_serial;
int state = BLACK;
void setup() {
  Serial.begin(115200);               // Set up serial port
  pinMode(PIN_1, INPUT_PULLUP);
  primary_timer = micros();
  render_counter = 0;
  tft.init();  //init screen
  tft.setRotation(2); //adjust rotation
  tft.setTextSize(1); //default font size
  tft.fillScreen(TFT_BLACK); //fill background
  tft.setTextColor(TFT_GREEN, TFT_BLACK); //set col
  analogSetAttenuation(ADC_6db); //set to 6dB attenuation for 3.3V full scale reading.
  change = millis();
}

void loop() {
  //  while (digitalRead(PIN_1)) {
  render_counter++;
  if (render_counter % UPDATE_PERIOD == 0) {
    raw_reading = analogRead(A0);
    scaled_reading_for_lcd = scaled_reading_for_serial * SCREEN_YMAX / (3.3);
    scaled_reading_for_serial = raw_reading * 3.3 / 4096;
    Serial.println(scaled_reading_for_serial);



    switch (state) {
      case BLACK:
        // fills screen blue
        tft.fillScreen(TFT_BLUE);
        state = C1;
        break;
      case C1:
        // checks if there is a clap after a rest period so we dont account for the last clap
        if (abs(scaled_reading_for_serial - 2) > thesh && millis() - change > 50 )
        {
          state = C2;
          change = millis();
        }

        break;
      case C2:
        // checks if there is continuous noise
        if (abs(scaled_reading_for_serial - 2) > thesh && millis() - change > 50 && millis() - change < 200)
        {
          state = C1;
        }
        //checks if there is a clap in the appropriate time range
        else if (abs(scaled_reading_for_serial - 2) > thesh && millis() - change > 200 &&  millis() - change < 750 )
        {
          state = COLOR;
        }
        //revert back to first listen state if more than 750 ms
        else if ( millis() - change > 750)
        {
          state  = C1;
        }
        break;
      case COLOR:
        //fill screen red
        tft.fillScreen(TFT_RED);
        state = B1;
        change = millis();
        break;
      case B1:
        // checks if there is a clap after a rest period so we dont account for the last clap
        if (abs(scaled_reading_for_serial - 2) > thesh && millis() - change > 100)
        {
          state = B2;
          change = millis();
        }


        break;
      case B2:
        // checks if there is continuous noise
        if (abs(scaled_reading_for_serial - 2) > thesh && millis() - change > 50 && millis() - change < 200)
        {
          state = B1;
        }
        //checks if there is a clap in the appropriate time range
        else if (abs(scaled_reading_for_serial - 2) > thesh && millis() - change > 200 &&  millis() - change < 750 )
        {
          state = BLACK;
          change = millis();
        }
        //revert back to first listen state if more than 750 ms
        else if ( millis() - change > 750)
        {
          state  = B1;
        }
        break;
    }

    
    old_scaled_reading_for_lcd = scaled_reading_for_lcd; //remember, remember the scaled_reading_for_lcd
  }




}
