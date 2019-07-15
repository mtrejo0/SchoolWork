#include<Wire.h>
#include<string.h>
#include <TFT_eSPI.h> // Graphics and font library for ST7735 driver chip
#include <SPI.h>

TFT_eSPI tft = TFT_eSPI();  //Make instance of TFT object

HardwareSerial gps(2); //instantiate approporiate Serial object for GPS

uint32_t timer; //used for loop timing
const uint16_t LOOP_PERIOD = 50; //period of system

const int BUFFER_LENGTH = 200;  //size of char array we'll use for
char buffer[BUFFER_LENGTH] = {0}; //dump chars into the

int lat_deg; //degrees portion of lattitude
int lat_dmF; //latitude decimal minutes
int lat_dmL; //latitude decimal minutes
char lat_dir; //latitude direction
int lon_deg; //longitude in degrees
int lon_dmF; //longitude decimal minutes
int lon_dmL; //longitude decimal minutes
char lon_dir; //longitude direction
int year; //year
int month; //month
int day; //day of month
int hour; //hour (24 clock GMT)
int minute; //minute
int second; //second
bool valid; //is the data valid

void setup() {
  Serial.begin(115200);
  tft.init(); //initialize the screen
  tft.setRotation(2); //set rotation for our layout
  tft.fillScreen(TFT_BLACK);
  tft.setTextColor(TFT_GREEN, TFT_BLACK);
  gps.begin(9600, SERIAL_8N1, 32, 33);
  timer = millis();
}

void loop() {
  //displayAllGPS();
  extractGNRMC();
  tft.setCursor(0, 0, 1);
  char info[200] = {0};

  if (valid) {
    sprintf(info, "Date: %02d/%02d/%02d\nTime: %02d:%02d:%02d\nLat: %d %d.%d'%c\nLon:%d %d.%d'%c", day, month, year, hour, minute, second, lat_deg, lat_dmF,lat_dmL, lat_dir, lon_deg, lon_dmF,lon_dmL, lon_dir);
  } else {
    sprintf(info, "No valid Fix       \n                 \n                  \n                   \n               \n            ");
  }
  tft.print(info);

  //Serial.println(info); //for debugging
  while (millis() - timer < LOOP_PERIOD); //pause
  timer = millis();
}

void displayAllGPS() {
  while (gps.available()) {     // If anything comes in Serial1 (pins 0 & 1)
    gps.readBytesUntil('\n', buffer, BUFFER_LENGTH); // read it and send it out Serial (USB)
    Serial.println(buffer);
  }
}

void extractGNRMC() {
  while (gps.available()) {     // If anything comes in Serial1 (pins 0 & 1)
    gps.readBytesUntil('\n', buffer, BUFFER_LENGTH); // read it and send it out Serial (USB)
    char* info = strstr(buffer, "GNRMC");
    if (info != NULL) {
      Serial.println(buffer);
      extract(buffer);
    }
  }
}

void extract(char* data_array) {
  String raw(data_array);
  String vals[15];

  int i = 0 ;
  int j = 0 ;
  int k = 0;
  while ( i < raw.length() )
  {
    if (i == 0 )
    {
      j = 0 ;
    }
    else if (raw.charAt(i) == ',')
    {
      vals[k] = raw.substring(j, i);

      j = i + 1;
      k++;
    }
    i++;
  }
  for (int a = 0 ; a < 15 ; a++)
  {
    Serial.println(vals[a]);
  }

  if(vals[2].charAt(0) == 'A')
  {
    valid = true;
  }
  else
  {
    valid = false;
  }

  lat_deg = vals[3].substring(0, 2).toInt();
  lat_dmF = vals[3].substring(2,4).toInt();
  lat_dmL =vals[3].substring(5).toInt();
  lat_dir = vals[4].charAt(0);

  lon_deg = vals[5].substring(1, 3).toInt();
  lon_dmF = vals[5].substring(3,5).toInt();
  lon_dmL = vals[5].substring(6).toInt();
  lon_dir = vals[6].charAt(0);

  year = vals[9].substring(4, 6).toInt();
  month = vals[9].substring(2, 4).toInt();
  day = vals[9].substring(0, 2).toInt();

  hour = vals[1].substring(0, 2).toInt();
  minute = vals[1].substring(2, 4).toInt();
  second = vals[1].substring(4, 6).toInt();




}
