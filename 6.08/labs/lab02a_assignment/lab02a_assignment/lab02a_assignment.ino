#include <mpu9255_esp32.h>
#include<math.h>
#include<string.h>
#include <TFT_eSPI.h> // Graphics and font library for ST7735 driver chip
#include <SPI.h>
TFT_eSPI tft = TFT_eSPI();  // Invoke library, pins defined in User_Setup.h


uint8_t state;
int steps;
float old_acc_mag, older_acc_mag;


const uint8_t LOOP_PERIOD = 10; //milliseconds
uint32_t primary_timer = 0;
float x,y,z; //variables for grabbing x,y,and z values

MPU9255 imu; //imu object called, appropriately, imu

void setup() {
  Serial.begin(115200); //for debugging if needed.
  delay(50); //pause to make sure comms get set up
  Wire.begin();
  delay(50); //pause to make sure comms get set up
  if (imu.setupIMU(1)){
    Serial.println("IMU Connected!");
  }else{
    Serial.println("IMU Not Connected :/");
    Serial.println("Restarting");
    ESP.restart(); // restart the ESP (proper way)
  }
  tft.init(); //initialize the screen
  tft.setRotation(2); //set rotation for our layout
  primary_timer = millis();
  tft.fillScreen(TFT_BLACK); 
  tft.setTextColor(TFT_BLUE, TFT_BLACK);
  steps = 0; //initialize steps to zero!
}

void loop() {
  imu.readAccelData(imu.accelCount);
  x = imu.accelCount[0]*imu.aRes;
  y = imu.accelCount[1]*imu.aRes;
  z = imu.accelCount[2]*imu.aRes;

  float acc_mag = 0;
  float avg_acc_mag = 0;

  
  //Serial printing:
  char output[80];
  float zoom = 10; //for zooming plot
  sprintf(output,"%4.2f,%4.2f",zoom*acc_mag,zoom*avg_acc_mag); //render numbers with %4.2 float formatting
  Serial.println(output); //print to serial for plotting

  //LCD Display:
  for(int i =0; i<3; i++){
    sprintf(output,"%4.2f",imu.accelCount[i]*imu.aRes);
    tft.drawString(output,0,10*i+10,1);
  }
  while (millis()-primary_timer<LOOP_PERIOD); //wait for primary timer to increment
  primary_timer =millis();
}
