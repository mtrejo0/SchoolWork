#include <math.h>
#include <SPI.h>
#include <TFT_eSPI.h>

TFT_eSPI tft = TFT_eSPI();

const int WIFI_COLOR = TFT_BLUE;
const int BATT_COLOR = TFT_PINK;
const int LED_COLOR = TFT_RED;
const int GPS_COLOR = TFT_PINK;
const int BACKGROUND = TFT_YELLOW;

//Power Variables
uint8_t power_state; //state of power state machine (0:
float old_discharge_amt; //previous discharge amount (used for calculating rate)
float discharge_rate; //estimated discharge rate
float time_remaining; //amount of time remaining until battery discharged


//pins for control:
const uint8_t BACKLIGHT = 14;
const uint8_t GPS_POWER = 12;

const uint32_t USAGE_PERIOD = 30000;
uint32_t usage_counter;

//Button Variables:
const int INPUT_PIN = 16; //the button's pin
uint8_t old_input; //used to remember previous button value (for edge detection)
uint8_t button_count; //for counting pushes (cycles through three power states)

//Loop Timing Variables:
const uint32_t LOOP_PERIOD = 40; //(ms)..how quickly primary loop iterates
uint32_t timer; //used for timing loop


double max(double first, double sec) {
  if (first > sec) return first;
  else return sec;
}

//renders a art-deco interpretation of the classic "WiFi" symbol (function for reference in lab07b)
void drawWiFi(TFT_eSPI* screen, uint8_t x, uint8_t y, uint16_t fc, uint16_t bc) {
  screen->drawCircle(x, y, 8, fc);
  screen->drawCircle(x, y, 6, fc);
  screen->drawCircle(x, y, 4, fc);
  screen->fillCircle(x, y, 2, fc);
  screen->fillRect(x - 8, y - 8, 8, 16, bc);
  screen->fillRect(x - 2, y + 1, 11, 10, bc);
}

//renders a gorgeous twinkle drawing...perhaps used to indicate some external light is on (function for reference in lab07b)
void drawLED(TFT_eSPI* screen, uint8_t x, uint8_t y, uint16_t fc, uint16_t bc) {
  screen->fillCircle(x, y, 2, fc);
  for (uint8_t i = 0; i < 8; i++) {
    screen->drawLine(x + 4 * sin(i * 2 * PI / 8), y - 4 * cos(i * 2 * PI / 8), x + 7 * sin(i * 2 * PI / 8), y - 7 * cos(i * 2 * PI / 8), fc);
  }
}


//renders battery symbol including level amount
void drawBattery(TFT_eSPI* screen, uint8_t x, uint8_t y, float level, uint16_t fc, uint16_t bc) {
  //YOUR CODE HERE, FRIEND
  tft.drawRect(x,y,20,8,TFT_BLACK);
  tft.fillRect(x+20,y+2,2,4,TFT_BLACK);
  tft.fillRect(x,y,level/4.2*20,8,TFT_BLACK);
}


//hand in a discharge amount, and generate a voltage

double voltage_from_discharge(double discharge){
  //your code here 
  double x = discharge;
//  double ans =  pow(x,4)*-5.08321149-pow(x,3)*-8.16962756+ pow(x,2)*-3.53049671-pow(x,1)*0.3295403+pow(x,0)* 4.08151442;
double ans = (((-5.08321149*x+8.16962756)*x-3.53049671)*x-0.3295403)*x+4.08151442;
  return ans;
  // [-5.08321149  8.16962756 -3.53049671 -0.3295403   4.08151442]
}

///nice binary-search...much quicker!
double discharge_from_voltage(double voltage, double error){
  //your code here!
  
  double temp = .5;
  double range = .5;
  double val = voltage_from_discharge(temp);
  for(int i = 0 ; i < 10 ; i ++)
  {
    if(fabs(val - voltage)<error)
    {
      return temp;
    }
    else if(val<voltage){
      temp = temp - range/2;
      range = range/2;
      val = voltage_from_discharge(temp);
    }
    else
    {
      temp = temp + range/2;
      range = range/2;
      val = voltage_from_discharge(temp);
    }
  }
  return temp;
   
}

void setup() {
  Serial.begin(115200);  // Set up serial port
  delay(300); //wait a bit (100 ms)
  pinMode(INPUT_PIN, INPUT_PULLUP);
  uint8_t count = 0; //count used for Wifi check times
  tft.init();  //init screen
  tft.setRotation(2); //adjust rotation
  tft.setTextSize(1); //default font size
  tft.fillScreen(BACKGROUND); //fill background
  tft.setTextColor(TFT_BLACK, BACKGROUND); //set color of font to green foreground, black background
  timer = millis();
  //initialize switch value:

  //initialize power variables:
  drawWiFi(&tft, 8, 12, WIFI_COLOR, BACKGROUND); //draw WiFi!
  drawLED(&tft, 25, 10, LED_COLOR, BACKGROUND); //draw LED!
  discharge_rate = 0.00001; //initialize dummy value
  time_remaining = -1; //initialize dummy value
  usage_counter = millis();
}

void loop() {
//  Serial.println(analogRead(A6));
  uint32_t start = micros(); //MARK BEGINNING OF TIMING!
  float voltage = analogRead(A6)*3.3*2/4096; // get Battery Voltage (mV)
  float discharge_amt = discharge_from_voltage(voltage, 0.001); //get discharge amount using battery voltage
  uint32_t diff = micros() - start; //MARK ENDING OF TIMING!
  Serial.println(diff); //PRINT DIFFERENCE IN MICROSECONDS!
  char battery_stats[200];
  uint32_t spot = sprintf(battery_stats, "Batt Voltage: %1.3fV\n", voltage);
  sprintf(battery_stats + spot, "Discharge Amt: %1.3f\n", discharge_amt);
  tft.setCursor(0, 31, 1);
  tft.print(battery_stats);
  drawBattery(&tft, 104, 3, 1.0 - discharge_amt, BATT_COLOR, BACKGROUND);
  while (millis() - timer < LOOP_PERIOD);
  timer = millis();
}
