#include <TFT_eSPI.h> // Graphics and font library for ST7735 driver chip
#include <SPI.h> //Used in support of TFT Display
#include <string.h>  //used for some string handling and processing.
#include <mpu9255_esp32.h>

TFT_eSPI tft = TFT_eSPI();  // Invoke library, pins defined in User_Setup.h

#define BACKGROUND TFT_GREEN
#define BALL_COLOR TFT_BLUE
#define pressed 1
#define unpressed 2

#define stillPressed 3
#define notStillPressed 4




const int DT = 40; //milliseconds
const int EXCITEMENT = 100000; //how much force to apply to ball
const uint8_t pin1 = 16; //CHANGE YOUR WIRING TO PIN 16!!! (FROM 19)
const uint8_t pin2 = 5;
uint32_t primary_timer; //main loop timer

int state = unpressed;
int past = unpressed;
int isPress = notStillPressed;
int numballs = 0;
float avgY = 0;
float avgX = 0;

//state variables:
float x_pos1 = 64; //x position
float y_pos1 = 80; //y position
float x_vel1 = 0; //x velocity
float y_vel1 = 0; //y velocity
float x_accel1 = 0; //x acceleration
float y_accel1 = 0; //y acceleration

float x_pos2 = 64; //x position
float y_pos2 = 80; //y position
float x_vel2 = 0; //x velocity
float y_vel2 = 0; //y velocity
float x_accel2 = 0; //x acceleration
float y_accel2 = 0; //y acceleration

float x_pos3 = 64; //x position
float y_pos3 = 80; //y position
float x_vel3 = 0; //x velocity
float y_vel3 = 0; //y velocity
float x_accel3 = 0; //x acceleration
float y_accel3 = 0; //y acceleration

float x_pos4 = 64; //x position
float y_pos4 = 80; //y position
float x_vel4 = 0; //x velocity
float y_vel4 = 0; //y velocity
float x_accel4 = 0; //x acceleration
float y_accel4 = 0; //y acceleration


float valuesX[50];
float valuesY[50];

boolean ball1 = false;
boolean ball2 = false;
boolean ball3 = false;
boolean ball4 = false;

//physics constants:
const float MASS = 1; //for starters
const int RADIUS = 5; //radius of ball
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
void step1(float x_force = 0, float y_force = 0 ) {
  //update acceleration (from f=ma)

  x_force = x_force - x_vel1 * K_FRICTION;
  y_force = y_force - y_vel1 * K_FRICTION;


  x_accel1 = x_force / MASS;
  y_accel1 = y_force / MASS;

  //integrate to get velocity from current acceleration
  x_vel1 = x_vel1 + 0.001 * DT * x_accel1; //integrate, 0.001 is conversion from milliseconds to seconds
  y_vel1 = y_vel1 + 0.001 * DT * y_accel1; //integrate!!
  moveBall1(); //you'll write this from scratch!
}
void moveBall1() {
  //Your code here!
  x_pos1 = x_pos1 + x_vel1 * DT / 1000;
  y_pos1 = y_pos1 + y_vel1 * DT / 1000;


  if (x_pos1 > RIGHT_LIMIT)
  {
    x_vel1 = -x_vel1 * K_SPRING;
    x_pos1 = x_pos1 - (x_pos1 - RIGHT_LIMIT) - (x_pos1 - RIGHT_LIMIT) * K_SPRING;
  }

  if (x_pos1 < LEFT_LIMIT)
  {
    x_vel1 = -x_vel1 * K_SPRING;
    x_pos1 = x_pos1 + (LEFT_LIMIT - x_pos1) + (LEFT_LIMIT - x_pos1) * K_SPRING;
  }
  if (y_pos1 > BOTTOM_LIMIT)
  {
    y_vel1 = -y_vel1 * K_SPRING;
    y_pos1 = y_pos1 - (y_pos1 - BOTTOM_LIMIT) - (y_pos1 - BOTTOM_LIMIT) * K_SPRING;
  }

  if (y_pos1 < TOP_LIMIT)
  {
    y_vel1 = -y_vel1 * K_SPRING;
    y_pos1 = y_pos1 + (TOP_LIMIT - y_pos1) + (TOP_LIMIT - y_pos1) * K_SPRING;
  }
}
//will eventually replace with your improved step function!
void step2(float x_force = 0, float y_force = 0 ) {
  //update acceleration (from f=ma)

  x_force = x_force - x_vel2 * K_FRICTION;
  y_force = y_force - y_vel2 * K_FRICTION;


  x_accel2 = x_force / MASS;
  y_accel2 = y_force / MASS;

  //integrate to get velocity from current acceleration
  x_vel2 = x_vel2 + 0.001 * DT * x_accel2; //integrate, 0.001 is conversion from milliseconds to seconds
  y_vel2 = y_vel2 + 0.001 * DT * y_accel2; //integrate!!
  moveBall2(); //you'll write this from scratch!
}
void moveBall2() {
  //Your code here!
  x_pos2 = x_pos2 + x_vel2 * DT / 1000;
  y_pos2 = y_pos2 + y_vel2 * DT / 1000;


  if (x_pos2 > RIGHT_LIMIT)
  {
    x_vel2 = -x_vel2 * K_SPRING;
    x_pos2 = x_pos2 - (x_pos2 - RIGHT_LIMIT) - (x_pos2 - RIGHT_LIMIT) * K_SPRING;
  }

  if (x_pos2 < LEFT_LIMIT)
  {
    x_vel2 = -x_vel2 * K_SPRING;
    x_pos2 = x_pos2 + (LEFT_LIMIT - x_pos2) + (LEFT_LIMIT - x_pos2) * K_SPRING;
  }
  if (y_pos2 > BOTTOM_LIMIT)
  {
    y_vel2 = -y_vel2 * K_SPRING;
    y_pos2 = y_pos2 - (y_pos2 - BOTTOM_LIMIT) - (y_pos2 - BOTTOM_LIMIT) * K_SPRING;
  }

  if (y_pos2 < TOP_LIMIT)
  {
    y_vel2 = -y_vel2 * K_SPRING;
    y_pos2 = y_pos2 + (TOP_LIMIT - y_pos2) + (TOP_LIMIT - y_pos2) * K_SPRING;
  }
}
//will eventually replace with your improved step function!
void step3(float x_force = 0, float y_force = 0 ) {
  //update acceleration (from f=ma)

  x_force = x_force - x_vel3 * K_FRICTION;
  y_force = y_force - y_vel3 * K_FRICTION;


  x_accel3 = x_force / MASS;
  y_accel3 = y_force / MASS;

  //integrate to get velocity from current acceleration
  x_vel3 = x_vel3 + 0.001 * DT * x_accel3; //integrate, 0.001 is conversion from milliseconds to seconds
  y_vel3 = y_vel3 + 0.001 * DT * y_accel3; //integrate!!
  moveBall3(); //you'll write this from scratch!
}
void moveBall3() {
  //Your code here!
  x_pos3 = x_pos3 + x_vel3 * DT / 1000;
  y_pos3 = y_pos3 + y_vel3 * DT / 1000;


  if (x_pos3 > RIGHT_LIMIT)
  {
    x_vel3 = -x_vel3 * K_SPRING;
    x_pos3 = x_pos3 - (x_pos3 - RIGHT_LIMIT) - (x_pos3 - RIGHT_LIMIT) * K_SPRING;
  }

  if (x_pos3 < LEFT_LIMIT)
  {
    x_vel3 = -x_vel3 * K_SPRING;
    x_pos3 = x_pos3 + (LEFT_LIMIT - x_pos3) + (LEFT_LIMIT - x_pos3) * K_SPRING;
  }
  if (y_pos3 > BOTTOM_LIMIT)
  {
    y_vel3 = -y_vel3 * K_SPRING;
    y_pos3 = y_pos3 - (y_pos3 - BOTTOM_LIMIT) - (y_pos3 - BOTTOM_LIMIT) * K_SPRING;
  }

  if (y_pos3 < TOP_LIMIT)
  {
    y_vel3 = -y_vel3 * K_SPRING;
    y_pos3 = y_pos3 + (TOP_LIMIT - y_pos3) + (TOP_LIMIT - y_pos3) * K_SPRING;
  }
}
//will eventually replace with your improved step function!
void step4(float x_force = 0, float y_force = 0 ) {
  //update acceleration (from f=ma)

  x_force = x_force - x_vel4 * K_FRICTION;
  y_force = y_force - y_vel4 * K_FRICTION;


  x_accel4 = x_force / MASS;
  y_accel4 = y_force / MASS;

  //integrate to get velocity from current acceleration
  x_vel4 = x_vel4 + 0.001 * DT * x_accel4; //integrate, 0.001 is conversion from milliseconds to seconds
  y_vel4 = y_vel4 + 0.001 * DT * y_accel4; //integrate!!
  moveBall4(); //you'll write this from scratch!
}
void moveBall4() {
  //Your code here!
  x_pos4 = x_pos4 + x_vel4 * DT / 1000;
  y_pos4 = y_pos4 + y_vel4 * DT / 1000;


  if (x_pos4 > RIGHT_LIMIT)
  {
    x_vel4 = -x_vel4 * K_SPRING;
    x_pos4 = x_pos4 - (x_pos4 - RIGHT_LIMIT) - (x_pos4 - RIGHT_LIMIT) * K_SPRING;
  }

  if (x_pos4 < LEFT_LIMIT)
  {
    x_vel4 = -x_vel4 * K_SPRING;
    x_pos4 = x_pos4 + (LEFT_LIMIT - x_pos4) + (LEFT_LIMIT - x_pos4) * K_SPRING;
  }
  if (y_pos4 > BOTTOM_LIMIT)
  {
    y_vel4 = -y_vel4 * K_SPRING;
    y_pos4 = y_pos4 - (y_pos4 - BOTTOM_LIMIT) - (y_pos4 - BOTTOM_LIMIT) * K_SPRING;
  }

  if (y_pos4 < TOP_LIMIT)
  {
    y_vel4 = -y_vel4 * K_SPRING;
    y_pos4 = y_pos4 + (TOP_LIMIT - y_pos4) + (TOP_LIMIT - y_pos4) * K_SPRING;
  }
}
void setup() {
  Serial.begin(115200); //for debugging if needed.
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

  pushed_last_time = false;
  primary_timer = millis();
  pinMode(pin1, INPUT_PULLUP);
  pinMode(pin2, INPUT_PULLUP);
}

void loop() {
  if (!digitalRead(pin2))
  {
    x_pos1 = 64; //x position
    y_pos1 = 80; //y position
    x_vel1 = 0; //x velocity
    y_vel1 = 0; //y velocity
    x_accel1 = 0; //x acceleration
    y_accel1 = 0; //y acceleration

    x_pos2 = 64; //x position
    y_pos2 = 80; //y position
    x_vel2 = 0; //x velocity
    y_vel2 = 0; //y velocity
    x_accel2 = 0; //x acceleration
    y_accel2 = 0; //y acceleration

    x_pos3 = 64; //x position
    y_pos3 = 80; //y position
    x_vel3 = 0; //x velocity
    y_vel3 = 0; //y velocity
    x_accel3 = 0; //x acceleration
    y_accel3 = 0; //y acceleration

    x_pos4 = 64; //x position
    y_pos4 = 80; //y position
    x_vel4 = 0; //x velocity
    y_vel4 = 0; //y velocity
    x_accel4 = 0; //x acceleration
    y_accel4 = 0; //y acceleration
    ball1 = false;
    ball2 = false;
    ball3 = false;
    ball4 = false;
    numballs = 0;
     tft.fillScreen(BACKGROUND);
  }
  if (!digitalRead(pin1))
  {

    past = state;
    state = pressed;
  }
  else
  {
    past = state;
    state = unpressed;
  }


  if (state == pressed && state == past)
  {
    imu.readAccelData(imu.accelCount);

    avgX = averaging_filter(imu.accelCount[1] * imu.aRes, valuesX, 40);
    avgY = averaging_filter(imu.accelCount[0] * imu.aRes, valuesY, 40);

  }

  if (past == pressed && state == unpressed)
  {
    for (int i = 0; i < 50 ; i++)
    {
      valuesX[i] = 0;
      valuesY[i] = 0;
    }

    switch (numballs) {
      case 0:
        step1(avgX * EXCITEMENT, avgY * EXCITEMENT);
        ball1 = true;
        numballs++;
        break;
      case 1:
        step2(avgX * EXCITEMENT, avgY * EXCITEMENT);
        ball2 = true;
        numballs++;
        break;
      case 2:
        step3(avgX * EXCITEMENT, avgY * EXCITEMENT);
        ball3 = true;
        numballs++;
        break;
      case 3:
        step4(avgX * EXCITEMENT, avgY * EXCITEMENT);
        ball4 = true;
        numballs++;
        break;

    }


  }




  if (ball1) {
    //draw circle in previous location of ball in color background (redraws minimal num of pixels, therefore is quick!)
    tft.fillCircle(x_pos1, y_pos1, RADIUS, BACKGROUND);
    step1();
    tft.fillCircle(x_pos1, y_pos1, RADIUS, TFT_BLUE); //draw new ball location
  }
  if (ball2) {
    //draw circle in previous location of ball in color background (redraws minimal num of pixels, therefore is quick!)
    tft.fillCircle(x_pos2, y_pos2, RADIUS, BACKGROUND);
    step2();
    tft.fillCircle(x_pos2, y_pos2, RADIUS, TFT_RED); //draw new ball location
  }
  if (ball3) {
    //draw circle in previous location of ball in color background (redraws minimal num of pixels, therefore is quick!)
    tft.fillCircle(x_pos3, y_pos3, RADIUS, BACKGROUND);
    step3();
    tft.fillCircle(x_pos3, y_pos3, RADIUS, TFT_YELLOW); //draw new ball location
  }
  if (ball4) {
    //draw circle in previous location of ball in color background (redraws minimal num of pixels, therefore is quick!)
    tft.fillCircle(x_pos4, y_pos4, RADIUS, BACKGROUND);
    step4();
    tft.fillCircle(x_pos4, y_pos4, RADIUS, TFT_PURPLE); //draw new ball location
  }

  while (millis() - primary_timer < DT); //wait for primary timer to increment
  primary_timer = millis();
}


float averaging_filter(float input, float* stored_values, int order) {
  for ( int i = 49 ; i > 0; i--)
  {
    stored_values[i] = stored_values[i - 1];
  }
  stored_values[0] = input;
  float val  = 0 ;
  for (int j = 0 ; j <= order ; j++)
  {
    val = val + (stored_values[j] * 1.0) / (1 + order);
  }
  return val;
}
