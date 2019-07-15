#include <TFT_eSPI.h> // Graphics and font library for ST7735 driver chip
#include <SPI.h> //Used in support of TFT Display
#include <string.h>  //used for some string handling and processing.
#include <mpu9255_esp32.h>

TFT_eSPI tft = TFT_eSPI();  // Invoke library, pins defined in User_Setup.h

#define BACKGROUND TFT_GREEN
#define BALL_COLOR TFT_BLUE

const int DT = 10; //milliseconds
const int EXCITEMENT = 1000; //how much force to apply to ball
const uint8_t BUTTON_PIN = 16; //CHANGE YOUR WIRING TO PIN 16!!! (FROM 19)

char positions[1000];

uint32_t primary_timer; //main loop timer

//state variables:
float x_pos = 64; //x position
float y_pos = 80; //y position
float x_vel = 0; //x velocity
float y_vel = 0; //y velocity
float x_accel = 0; //x acceleration
float y_accel = 0; //y acceleration
const char USER[] = "moises";
const uint8_t pin1 = 16; //CHANGE YOUR WIRING TO PIN 16!!! (FROM 19)
const uint8_t pin2 = 5;
const uint16_t IN_BUFFER_SIZE = 1000; //size of buffer to hold HTTP request
const uint16_t OUT_BUFFER_SIZE = 1000; //size of buffer to hold HTTP response
char request_buffer[IN_BUFFER_SIZE]; //char array buffer to hold HTTP request
char response_buffer[OUT_BUFFER_SIZE]; //char array buffer to hold HTTP response
const int RESPONSE_TIMEOUT = 6000; //ms to wait for response from host
const int POSTING_PERIOD = 6000; //periodicity of getting a number fact.
//physics constants:
const float MASS = 1; //for starters
const int RADIUS = 2; //radius of ball
const float K_FRICTION = 0.15;  //friction coefficient
const float K_SPRING = 0.9;  //spring coefficient

//boundary constants:
const int LEFT_LIMIT = RADIUS; //left side of screen limit
const int RIGHT_LIMIT = 127 - RADIUS; //right side of screen limit
const int TOP_LIMIT = RADIUS; //top of screen limit
const int BOTTOM_LIMIT = 159 - RADIUS; //bottom of screen limit

bool pushed_last_time; //for finding change of button (using bool type...same as uint8_t)


MPU9255 imu; //imu object called, appropriately, imu

//will eventually replace with your improved step function!
void step(float x_force = 0, float y_force = 0) {
  //Your code here!

  //update acceleration (from f=ma)
  x_force = x_force - x_vel * K_FRICTION;
  y_force = y_force - y_vel * K_FRICTION;


  x_accel = x_force / MASS;
  y_accel = y_force / MASS;

  //integrate to get velocity from current acceleration
  x_vel = x_vel + 0.001 * DT * x_accel; //integrate, 0.001 is conversion from milliseconds to seconds
  y_vel = y_vel + 0.001 * DT * y_accel; //integrate!!



  moveBall(); //you'll write this from scratch!
}
void moveBall() {
  //Your code here!
  x_pos = x_pos + x_vel * DT / 1000;
  y_pos = y_pos + y_vel * DT / 1000;


  if (x_pos > RIGHT_LIMIT)
  {
    x_vel = 0;
    x_pos = x_pos - (x_pos - RIGHT_LIMIT) - (x_pos - RIGHT_LIMIT) * K_SPRING;
  }

  if (x_pos < LEFT_LIMIT)
  {
    x_vel = 0;
    x_pos = x_pos + (LEFT_LIMIT - x_pos) + (LEFT_LIMIT - x_pos) * K_SPRING;
  }
  if (y_pos > BOTTOM_LIMIT)
  {
    y_vel = 0;
    y_pos = y_pos - (y_pos - BOTTOM_LIMIT) - (y_pos - BOTTOM_LIMIT) * K_SPRING;
  }

  if (y_pos < TOP_LIMIT)
  {
    y_vel = 0;
    y_pos = y_pos + (TOP_LIMIT - y_pos) + (TOP_LIMIT - y_pos) * K_SPRING;
  }
}

void setup() {
  Serial.begin(115200); //for debugging if needed.
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  tft.init();
  tft.setRotation(2);
  tft.setTextSize(1);
  tft.fillScreen(BACKGROUND);
  if (imu.setupIMU(1)) {
    Serial.println("IMU Connected!");
  } else {
    Serial.println("IMU Not Connected :/");
    Serial.println("Restarting");
    ESP.restart(); // restart the ESP (proper way)
  }
  randomSeed(analogRead(0));  //initialize random numbers
  step(random(-EXCITEMENT, EXCITEMENT), random(-EXCITEMENT, EXCITEMENT)); //apply initial force to lower right
  pushed_last_time = false;
  primary_timer = millis();
  pinMode(pin1, INPUT_PULLUP);
  pinMode(pin2, INPUT_PULLUP);
}

void loop() {
  //draw circle in previous location of ball in color background (redraws minimal num of pixels, therefore is quick!)
  //tft.fillCircle(x_pos,y_pos,RADIUS,BACKGROUND);
  //if button pushed *just* pushed down, inject random force into system
  //else, just run out naturally

  if (!digitalRead(pin1))
  {
    tft.fillScreen(BACKGROUND);
    for (int i = 0; i < 1000; i++)
    {
      positions[i] = 0;
    }
  }
  if (!digitalRead(pin2))
  {
    //post_request();
  }
  imu.readAccelData(imu.accelCount);//read imu
  float x = -imu.accelCount[1] * imu.aRes;
  float y = -imu.accelCount[0] * imu.aRes;
  step(x * EXCITEMENT, y * EXCITEMENT); //apply force from imu
  tft.fillCircle(x_pos, y_pos, RADIUS, BALL_COLOR); //draw new ball location

  char curr[20];
  sprintf(curr, "%f,%f&", x_pos, y_pos);
  strcat(positions, curr);
  Serial.println(positions);

  while (millis() - primary_timer < DT); //wait for primary timer to increment
  primary_timer = millis();
}

void post_request(float* arr) {
  char body[100]; //for body
  sprintf(body, positions, USER);
  int body_len = strlen(body); //calculate body length (for header reporting)
  sprintf(request_buffer, "POST /sandbox/etchsketch HTTP/1.1\r\n");
  strcat(request_buffer, "Host: 608dev.net\r\n");
  strcat(request_buffer, "Content-Type: application/json\r\n");

  sprintf(request_buffer + strlen(request_buffer), "Content-Length: %d\r\n", body_len); //append string formatted to end of request buffer
  strcat(request_buffer, "\r\n"); //new line from header to body
  strcat(request_buffer, body); //body
  strcat(request_buffer, "\r\n"); //header
  Serial.println(request_buffer);
  do_http_request("608dev.net", request_buffer, response_buffer, OUT_BUFFER_SIZE, RESPONSE_TIMEOUT, true);
  Serial.println(response_buffer); //viewable in Serial Terminal
}
