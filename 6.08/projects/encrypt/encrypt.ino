#include <TinyGPS++.h>
#include <WiFi.h> //Connect to WiFi Network
#include <TFT_eSPI.h> // Graphics and font library for ST7735 driver chip
#include <SPI.h> //Used in support of TFT Display
#include <string.h>  //used for some string handling and processing.


#define list 0
#define disp 1

TFT_eSPI tft = TFT_eSPI();  // Invoke library, pins defined in User_Setup.h

char network[] = "MIT";  //SSID for 6.08 Lab
char password[] = ""; //Password for 6.08 Lab
char body[200];

int state = list;
const uint8_t LOOP_PERIOD = 10; //milliseconds
uint32_t primary_timer = 0;
uint32_t posting_timer = 0;
float x, y, z; //variables for grabbing x,y,and z values

const char USER[] = "moises";

//Some constants and some resources:
const int RESPONSE_TIMEOUT = 6000; //ms to wait for response from host

const uint16_t IN_BUFFER_SIZE = 1000; //size of buffer to hold HTTP request
const uint16_t OUT_BUFFER_SIZE = 1000; //size of buffer to hold HTTP response
char request_buffer[IN_BUFFER_SIZE]; //char array buffer to hold HTTP request
char response_buffer[OUT_BUFFER_SIZE]; //char array buffer to hold HTTP response

const uint8_t PIN_1 = 16; //button 1
const uint8_t PIN_2 = 5; //button 2
float lat = 0;
float lon = 0;

HardwareSerial gps_serial(2);
TinyGPSPlus gps;

uint8_t old_val1; //for button edge detection!
uint8_t old_val2;
uint32_t timer;
int pointer = 0;

char output[500];
char options[100] = " 0 Weather\n 1 Time\n 2 Date\n 3 Visibility";
char pointerString[10];


void setup() {
  Serial.begin(115200);
  gps_serial.begin(9600, SERIAL_8N1, 32, 33);
  tft.init();  //init screen
  tft.setRotation(2); //adjust rotation
  tft.setTextSize(1); //default font size
  tft.fillScreen(TFT_BLACK); //fill background
  tft.setTextColor(TFT_GREEN, TFT_BLACK); //set color of font to green foreground, black background
  Serial.begin(115200); //begin serial comms
  delay(100); //wait a bit (100 ms)
  pinMode(PIN_1, INPUT_PULLUP);
  pinMode(PIN_2, INPUT_PULLUP);

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
  timer = millis();
  old_val1 = digitalRead(PIN_1);
  old_val2 = digitalRead(PIN_2);
  char encrypted_message[] = "Y|u'{ol'Ql~lsz'Sp}l'h{'{ol'Nhyklu(";
  char message[60];
  int shift = 7;
  caesar_cipher(encrypted_message, message, shift, false, 8);
  Serial.println(encrypted_message);

}

void caesar_cipher(char* message_in, char* message_out, int shift, bool encrypt, int out_buffer_size) {
  //your code here

  int low = 32;
  int high = 127;
  if (strlen(message_in) < out_buffer_size)
  {
    out_buffer_size = strlen(message_in);
  }
  for (int i = 0 ; i < out_buffer_size; i++)
  {
    if (encrypt) {
      *(message_out + i) = char((int(message_in[i]) - low + shift) % (high - low) + low);
    }
    else
    {
      *(message_out + i) = char((int(message_in[i]) - low - shift) % (high - low) + low);
    }

  }
}
void loop() {

  while (millis() - timer < LOOP_PERIOD);
  timer = millis();
}
