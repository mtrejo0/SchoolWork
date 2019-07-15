#include <WiFi.h> //Connect to WiFi Network
#include <TFT_eSPI.h> // Graphics and font library for ST7735 driver chip
#include <SPI.h> //Used in support of TFT Display
#include <string.h>  //used for some string handling and processing.

/*#########################################
  Simple example script demonstrating:
  Connection with an Access Point (AP)
  Creation of client object
  Connection of client object to host
  Sending of GET request with several arguments
  verbose printing of HTTP response from host
  Simple parsing of HTTP response

  We'll use the open API found at:
  http://numbersapi.com
  Intended for 6.08 Spring 2019 Lab 01B
*/

TFT_eSPI tft = TFT_eSPI();  // Invoke library, pins defined in User_Setup.h

const int RESPONSE_TIMEOUT = 6000; //ms to wait for response from host
const int GETTING_PERIOD = 5000; //periodicity of getting a number fact.
const uint16_t IN_BUFFER_SIZE = 1000; //size of buffer to hold HTTP request
const uint16_t OUT_BUFFER_SIZE = 1000; //size of buffer to hold HTTP response
char request_buffer[IN_BUFFER_SIZE]; //char array buffer to hold HTTP request
char response_buffer[OUT_BUFFER_SIZE]; //char array buffer to hold HTTP response

uint32_t loop_controller; //used for timing
uint32_t last_time; //used for timing

char network[] = "6s08";
char password[] = "iesc6s08";
//char network[] = "6s08";  //SSID for 6.08 Lab
//char password[] = "iesc6s08"; //Password for 6.08 Lab
const uint8_t input_pin1 = 16;
int hr = 0;
int mi = 0;
int sec = 0;
int timer = 0;
String digital = "";
String date = "";

void setup() {
  tft.init();
  tft.setRotation(2);
  tft.setTextSize(1);
  tft.fillScreen(TFT_BLACK);
  tft.setTextColor(TFT_GREEN, TFT_BLACK);
  Serial.begin(115200); //begin serial
  delay(100); //wait a bit (100 ms)
  WiFi.begin(network, password); //attempt to connect to wifi
  uint8_t count = 0; //count used for Wifi check times
  Serial.print("Attempting to connect to ");
  Serial.println(network);
  while (WiFi.status() != WL_CONNECTED && count < 6) {
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
  randomSeed(analogRead(A0)); //"seed" random number generator
  pinMode(input_pin1, INPUT_PULLUP);

}

/*-----------------------------------
   Generate a request to the numbersapi server for a random number
   Display the response both on the TFT and in the Serial Monitor
*/
void loop() {

  //formulate GET request...first line:
  sprintf(request_buffer, "GET http://608dev.net/sandbox/currenttime\r\n");
  strcat(request_buffer, "Host: 608dev.net\r\n"); //add more to the end
  strcat(request_buffer, "\r\n"); //add blank line!



  if (timer % 60 == 0 ) {
    do_http_GET("608dev.net", request_buffer, response_buffer, OUT_BUFFER_SIZE, RESPONSE_TIMEOUT, true);
    String str(response_buffer);
    digital = str.substring(11, 19);
    date = str.substring(0, 10);
    timer = 0;
    hr = digital.substring(0, 2).toInt();
    mi = digital.substring(3, 5).toInt();
    sec = digital.substring(6, 8).toInt();
    Serial.println("refresh");

  }
  else {
    int curr = millis();
    while (millis() - curr < 1000)
    {
      ;
    }

    sec++;
    if (sec > 59)
    {
      mi++;
      sec = 0;
    }
    if (mi > 59)
    {
      hr++;
      mi = 0;
    }
  }
  timer++;



  if (digitalRead(input_pin1)) {
    tft.fillScreen(TFT_BLACK); //black out TFT Screen
    tft.drawString(digital, 0, 0, 1); //viewable on Screen
    tft.drawString(date, 0, 20, 1);
    char output[40];
    if (hr > 12)
    {
      hr = hr - 12;
      Serial.println(hr);
    }
    sprintf(output, "%2.2d:%2.2d:%2.2d", hr, mi, sec);
    tft.drawString(output, 0, 0, 1);




  }
  else
  {
    tft.fillScreen(TFT_BLACK);
    tft.drawString(date, 0, 20, 1);

    for (int i = 0 ; i < 12 ; i++)
    {
      char output[40];
      sprintf(output, "%4.2d", i + 1);
      tft.drawString(output, 45 + 50 * cos(i / 12.0 * 2 * PI - PI / 2 + PI / 6), 95 + 50 * sin(i / 12.0 * 2 * PI - PI / 2 + PI / 6), 1);
    }
    tft.drawCircle(60, 100, 40, TFT_GREEN);
    if (hr > 12)
    {
      hr = hr - 12;
      Serial.println(hr);
    }
    tft.drawLine(60, 100, 60 + 20 * cos(hr / 12.0 * 2 * PI - PI / 2), 100 + 20 * sin(hr / 12.0 * 2 * PI - PI / 2), TFT_GREEN);
    tft.drawLine(60, 100, 60 + 30 * cos(mi / 60.0 * 2 * PI - PI / 2), 100 + 30 * sin(mi / 60.0 * 2 * PI - PI / 2), TFT_RED);
    tft.drawLine(60, 100, 60 + 40 * cos(sec / 60.0 * 2 * PI - PI / 2), 100 + 40 * sin(sec / 60.0 * 2 * PI - PI / 2), TFT_BLUE);





  }
}


/*----------------------------------
   char_append Function:
   Arguments:
      char* buff: pointer to character array which we will append a
      char c:
      uint16_t buff_size: size of buffer buff

   Return value:
      boolean: True if character appended, False if not appended (indicating buffer full)
*/
uint8_t char_append(char* buff, char c, uint16_t buff_size) {
  int len = strlen(buff);
  if (len > buff_size) return false;
  buff[len] = c;
  buff[len + 1] = '\0';
  return true;
}

/*----------------------------------
   do_http_GET Function:
   Arguments:
      char* host: null-terminated char-array containing host to connect to
      char* request: null-terminated char-arry containing properly formatted HTTP GET request
      char* response: char-array used as output for function to contain response
      uint16_t response_size: size of response buffer (in bytes)
      uint16_t response_timeout: duration we'll wait (in ms) for a response from server
      uint8_t serial: used for printing debug information to terminal (true prints, false doesn't)
   Return value:
      void (none)
*/
void do_http_GET(char* host, char* request, char* response, uint16_t response_size, uint16_t response_timeout, uint8_t serial) {
  WiFiClient client; //instantiate a client object
  if (client.connect(host, 80)) { //try to connect to host on port 80
    //if (serial) Serial.print(request);//Can do one-line if statements in C without curly braces
    client.print(request);
    memset(response, 0, response_size); //Null out (0 is the value of the null terminator '\0') entire buffer
    uint32_t count = millis();
    while (client.connected()) { //while we remain connected read out data coming back
      client.readBytesUntil('\n', response, response_size);

      //if (serial) Serial.println(response);

      if (millis() - count > response_timeout) break;
    }
    //empty in prep to store body
    count = millis();
    while (client.available()) { //read out remaining text (body of response)
      char_append(response, client.read(), OUT_BUFFER_SIZE);
    }
    //if (serial) Serial.println(response);

    client.stop();
    //if (serial) Serial.println("-----------");
  } else {
    if (serial) Serial.println("connection failed :/");
    if (serial) Serial.println("wait 0.5 sec...");
    client.stop();
  }
}
