//#include <Wire.h>
#include "PCA9685.h"

PCA9685 pwmController1(B000000);
//PCA9685 pwmController2(B000001);
PCA9685 pwmController2(B000010);
//PCA9685 pwmController3(B000011);

const unsigned long int i2c_freq = 115200;  // this is the max(?) i2c freq the arduino supports
//const unsigned long int serial_baudrate = 500000;
const unsigned long int serial_baudrate = 115200;
const unsigned int pwm_freq = 1600;

//#define I2C_FREQ 400000;
//#define SERIAL_BAUDRATE 500000;

byte temp[1];
byte buff[3];  // position byte, value byte, buffer byte
byte pos;
byte val;

unsigned x = 0;

int ab;

void setup() {

  Serial.begin(serial_baudrate);
  Serial.setTimeout(1);
  Wire.begin();
  
  pwmController1.resetDevices();       // Resets all PCA9685 devices on i2c line
  
  pwmController1.init();               // Initializes module using default totem-pole driver mode, and default phase balancer
  
  pwmController1.setPWMFrequency(500); // Set PWM freq to 500Hz (default is 200Hz, supports 24Hz to 1526Hz)
  
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB
  }
}

void read_serial_data(){
  Serial.readBytes(temp, 1);
  if (temp[0] == 0){
    read_serial_data();
  }
  return;
}

void read_end_byte(){
  Serial.readBytes(temp, 1);
  if (temp[0] != 255){
    read_end_byte();
  }
  return;
}


void loop() {

  if (Serial.available() > 0) {

    read_serial_data();
    buff[0] = temp[0];
    read_serial_data();
    buff[1] = temp[0];
    read_end_byte();
    buff[2] = temp[0];

    Serial.print(buff[0]);
    Serial.print(" ");
    Serial.print(buff[1]);
    Serial.print(" ");
    Serial.print(buff[2]);
    Serial.print('\n');
    
    buff[0] -= 1;
    buff[1] -= 1;
    
    if(0 <= buff[0] && buff[0] < 16){
        pwmController1.setChannelPWM(buff[0], buff[1] << 4);
    }
    
//    if(0 <= buff[0] && buff[0] < 16){
//        pwmController1.setChannelPWM(buff[0], buff[1] << 4);
//    } else if (16 <= buff[0] && buff[0] < 32){
//        pwmController2.setChannelPWM(buff[0], buff[1] << 4);
//    }


  
  }
}
