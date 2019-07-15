#include <SPI.h>
#include <TFT_eSPI.h>
TFT_eSPI tft = TFT_eSPI();

const int BUTTON_PIN = 16;

class Button {
  public:
    uint32_t t_of_state_2;
    uint32_t t_of_button_change;
    uint32_t debounce_time;
    uint32_t long_press_time;
    uint8_t pin;
    uint8_t flag;
    bool button_pressed;
    uint8_t state; // This is public for the sake of convenience
    Button(int p) {
      flag = 0;
      state = 0;
      pin = p;
      t_of_state_2 = millis(); //init
      t_of_button_change = millis(); //init
      debounce_time = 10;
      long_press_time = 1000;
      button_pressed = 0;
    }
    void read() {
      uint8_t button_state = digitalRead(pin);
      button_pressed = !button_state;
    }

    //feel free to use case instead of if-else-if!!
    int update() {
      read();
      flag = 0;
      //feel free to use case instead of if-else-if!!
      if (state == 0) {
        if (button_pressed) {
          state = 1;
          t_of_button_change = millis();
        }
      } else if (state == 1) {
        if (!(button_pressed)) {
          state = 0;
          t_of_button_change = millis();
        }
        else if (millis() - t_of_button_change >= debounce_time) {
          state = 2;
          t_of_state_2 = millis();
        }
      } else if (state == 2) {
        if ((button_pressed) and (millis() - t_of_state_2 >= long_press_time)) {
          state = 3;
        }
        else if (!(button_pressed)) {
          state = 4;
          t_of_button_change = millis();
        }
      } else if (state == 3) {
        if (!(button_pressed)) {
          state = 4;
          t_of_button_change = millis();
        }
      } else if (state == 4) {
        if ((button_pressed) and (millis() - t_of_state_2 < long_press_time)) {
          state = 2;
          t_of_button_change = millis();
        }
        else if ((button_pressed) and (millis() - t_of_state_2 >= long_press_time)) {
          state = 3;
          t_of_button_change = millis();
        }
        else if (!(button_pressed) and (millis() - t_of_button_change >= debounce_time)) {
          state = 0;
          if (millis() - t_of_state_2 >= long_press_time) {
            flag = 2;
          }
          else {
            flag = 1;
          }
        }
      }
      return flag;
    }
};

Button button(BUTTON_PIN);

void setup() {
  Serial.begin(115200);               // Set up serial port
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  tft.init();
  tft.setRotation(2);
  tft.setTextSize(1);
  tft.fillScreen(TFT_BLACK);

}

//delays are used here just for testing purposes!
// do not use delays in production
void loop() {
  tft.setCursor(0, 15, 1);
  uint8_t flag = button.update();
  Serial.println(flag);
  if (flag == 1) {
    tft.print("short press");
    delay(1000);  //bad practice...just for testing!
  } else if (flag == 2) {
    tft.print("long press");
    delay(1000); //bad practice...just for testing!
  } else {
    char temp_message[30];
    sprintf(temp_message, "%u          ", button.state); //for clearing out other messages
    tft.print(temp_message);
    delay(1);  //bad practice...just for testing.
  }
}
