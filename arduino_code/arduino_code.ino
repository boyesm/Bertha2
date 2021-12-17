//#include <Wire.h>
#include "PCA9685.h"

PCA9685 pwmController(B000000);

const unsigned long int i2c_freq = 400000;  // this is the max(?) i2c freq the arduino supports
//const unsigned long int serial_baudrate = 500000;
const unsigned long int serial_baudrate = 115200;
const unsigned int pwm_freq = 1600;

//#define I2C_FREQ 400000;
//#define SERIAL_BAUDRATE 500000;

byte buff[2];  // position byte, value byte

unsigned x = 0;

int ab;

void setup() {

  Serial.begin(serial_baudrate);
  Serial.setTimeout(1);
  Wire.begin();
  
  pwmController.resetDevices();       // Resets all PCA9685 devices on i2c line
  
  pwmController.init();               // Initializes module using default totem-pole driver mode, and default phase balancer
  
  pwmController.setPWMFrequency(500); // Set PWM freq to 500Hz (default is 200Hz, supports 24Hz to 1526Hz)
  
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB
  }
}



void loop() {

  if (Serial.available() > 0) {
  
    Serial.readBytes(buff, 2);
    
    Serial.print(buff[0]);
    Serial.print(" ");
    Serial.println(buff[1]);
    
    
    pwmController.setChannelPWM(buff[0], buff[1] << 4);
  
  }
}
