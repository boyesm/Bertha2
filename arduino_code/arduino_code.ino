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

  // pwmController.setChannelPWM(0, 128 << 4);
}



void loop() {

//  if (Serial.available() > 0) {
//     ab = Serial.readString().toInt();
//    ab = Serial.parseInt();
//     Serial.print(ab);
//    Serial.print("test!");
//  }

// /*

// append parse int to array
// when array is 2 long proceed

if (Serial.available() > 0) {

//  long int i = Serial.parseInt();

  Serial.readBytes(buff, 2);

  Serial.print(buff[0]);
  Serial.print(" ");
  Serial.println(buff[1]);
  

//  Serial.println(i);

//  if(x == 0){
//    buff[0] = i;
//    x=1;
//  } else if (x==1){
//    buff[1] = i;
//    x=0;
//
//    Serial.print(buff[0]);
//    Serial.print(" ");
//    Serial.println(buff[1]);
//
//    // no need to clear buffer
//
////    pwm1.setPWM(buff[0], buff[1], 0);
//
    pwmController.setChannelPWM(buff[0], buff[1] << 4);
//  }
//  

  
}

//*/
    
  

  


}
