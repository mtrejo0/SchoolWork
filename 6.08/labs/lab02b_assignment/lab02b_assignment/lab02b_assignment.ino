#include <WiFi.h> //Connect to WiFi Network
#include <TFT_eSPI.h> // Graphics and font library for ST7735 driver chip
#include <SPI.h> //Used in support of TFT Display
#include <string.h>  //used for some string handling and processing.
#include <mpu9255_esp32.h>
#include<math.h>

TFT_eSPI tft = TFT_eSPI();  // Invoke library, pins defined in User_Setup.h
#define IDLE 0
#define UP 1

#define DOWN 4
#define POST 5


char network[] = "MIT GUEST";  //SSID for 6.08 Lab
char password[] = ""; //Password for 6.08 Lab

const uint8_t LOOP_PERIOD = 10; //milliseconds
uint32_t primary_timer = 0;
uint32_t posting_timer = 0;
uint32_t step_timer = 0;
int steps = 0;
int total = 0;
float x, y, z; //variables for grabbing x,y,and z values

const float THRESHOLD = 1.2;
const int REFRACTORY = 200;

const char USER[] = "moises";

//Some constants and some resources:
const int RESPONSE_TIMEOUT = 6000; //ms to wait for response from host
const int POSTING_PERIOD = 6000; //periodicity of getting a number fact.
const uint16_t IN_BUFFER_SIZE = 1000; //size of buffer to hold HTTP request
const uint16_t OUT_BUFFER_SIZE = 1000; //size of buffer to hold HTTP response
char request_buffer[IN_BUFFER_SIZE]; //char array buffer to hold HTTP request
char response_buffer[OUT_BUFFER_SIZE]; //char array buffer to hold HTTP response




const uint8_t input_pin1 = 16; //pin connected to button
const uint8_t input_pin2 = 5; //pin connected to button


uint8_t state;  //system state for step counting
uint8_t post_state; //state of posting


MPU9255 imu; //imu object called, appropriately, imu

float old_acc_mag;
float older_acc_mag;  //


float old;


void setup() {
  tft.init();  //init screen
  tft.setRotation(2); //adjust rotation
  tft.setTextSize(1); //default font size
  tft.fillScreen(TFT_BLACK); //fill background
  tft.setTextColor(TFT_GREEN, TFT_BLACK); //set color of font to green foreground, black background
  Serial.begin(115200); //begin serial comms
  delay(100); //wait a bit (100 ms)
  Wire.begin();
  delay(50); //pause to make sure comms get set up
  if (imu.setupIMU(1)) {
    Serial.println("IMU Connected!");
  } else {
    Serial.println("IMU Not Connected :/");
    Serial.println("Restarting");
    ESP.restart(); // restart the ESP (proper way)
  }
  WiFi.begin(network, password); //attempt to connect to wifi
  uint8_t count = 0; //count used for Wifi check times
  Serial.print("Attempting to connect to ");
  Serial.println(network);
  while (WiFi.status() != WL_CONNECTED && count < 12) {
    delay(500);
    Serial.print(".");
    count++;
  }
  delay(2000);
  if (WiFi.isConnected()) { //if we connected then print our IP, Mac, and SSID we're on
    Serial.println("CONNECTED!");
    Serial.println(WiFi.localIP().toString() + " (" + WiFi.macAddress() + ") (" + WiFi.SSID() + ")");
    delay(500);
  } else { //if we failed to connect just Try again.
    Serial.println("Failed to Connect :/  Going to restart");
    Serial.println(WiFi.status());
    ESP.restart(); // restart the ESP (proper way)
  }
  pinMode(input_pin1, INPUT_PULLUP); //set input pin as an input!
  pinMode(input_pin2, INPUT_PULLUP); //set input pin as an input!
  state = IDLE;
  post_state = IDLE;
}


void loop() {
  //GET INPUT INFORMATION:
  imu.readAccelData(imu.accelCount);
  float x, y, z;
  x = imu.accelCount[0] * imu.aRes;
  y = imu.accelCount[1] * imu.aRes;
  z = imu.accelCount[2] * imu.aRes;
  uint8_t button1 = digitalRead(input_pin1);
  uint8_t button2 = digitalRead(input_pin2);
  float acc_mag = sqrt(x * x + y * y + z * z);
  float avg_acc_mag = 1.0 / 3.0 * (acc_mag + old_acc_mag + older_acc_mag);





  step_reporter_fsm(avg_acc_mag, acc_mag); //run step_reporter_fsm
  post_reporter_fsm(button1); //run post_reporter_fsm
  lcd_display(button2); //update display (minimize pixels you change)

  while (millis() - primary_timer < LOOP_PERIOD); //wait for primary timer to increment
  primary_timer = millis();
}


//Post reporting state machine, uses button1 as input
void post_reporter_fsm(uint8_t button1) {
  switch (post_state) {
    case IDLE:
      if (!button1)
      {
        post_state = DOWN;
      }
      break;
    case DOWN:
      if (button1)
      {
        post_state = POST;
      }
    case POST:
      Serial.println(steps); //print to serial for plotting
      char body[100]; //for body
      sprintf(body, "user=%s&steps=%d", USER, steps); //generate body, posting to User, 1 step
      int body_len = strlen(body); //calculate body length (for header reporting)
      sprintf(request_buffer, "POST http://608dev.net/sandbox/stepcounter HTTP/1.1\r\n");
      strcat(request_buffer, "Host: 608dev.net\r\n");
      strcat(request_buffer, "Content-Type: application/x-www-form-urlencoded\r\n");
      sprintf(request_buffer + strlen(request_buffer), "Content-Length: %d\r\n", body_len); //append string formatted to end of request buffer
      strcat(request_buffer, "\r\n"); //new line from header to body
      strcat(request_buffer, body); //body
      strcat(request_buffer, "\r\n"); //header
      Serial.println(request_buffer);
      do_http_request("608dev.net", request_buffer, response_buffer, OUT_BUFFER_SIZE, RESPONSE_TIMEOUT, true);
      Serial.println(response_buffer); //viewable in Serial Terminal
      steps = 0;
      post_state = IDLE;
      break;
  }

}

//Step Counting FSM from Lab02A.  (adapt global variables as needed!)
void step_reporter_fsm(float avg_acc_mag, float acc_mag) {

  //Serial printing:
  char output[80];
  float zoom = 1; //for zooming plot


  
  switch (state) {
    case IDLE:
      if (acc_mag - old_acc_mag > 0.14) {
        state = UP;
        steps++;
      }
      break;
    case UP:
      if (old_acc_mag - acc_mag > 0.14) {
        state = IDLE;
      }
      break;
  }


  while (millis() - primary_timer < LOOP_PERIOD); //wait for primary timer to increment
  primary_timer = millis();
  older_acc_mag = old_acc_mag;
  old_acc_mag = acc_mag;


}

//Display information on LED based on button value (stateless)
void lcd_display(uint8_t input) {
  if (input)
  {
    char output[80];
    sprintf(output, "STEPS: %4.2d", steps);
    tft.drawString(output, 0, 0, 1);
  }
  else
  {
    tft.fillScreen(TFT_BLACK);
    tft.drawString(response_buffer, 0, 0, 1);
  }

}
