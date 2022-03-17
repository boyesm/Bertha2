//#include <Wire.h>
#include "PCA9685.h"

PCA9685 pwmController1(B000000);
PCA9685 pwmController2(B000010);
PCA9685 pwmController3(B000001);

// Not a real device, will act as a proxy to pwmController1 and pwmController2, using all-call i2c address 0xE0, and default Wire @400kHz
PCA9685 pwmControllerAll(PCA9685_I2C_DEF_ALLCALL_PROXYADR);

#define I2C_FREQ 115200; // this is the max(?) i2c freq the arduino supports
#define SERIAL_BAUDRATE 115200;
#define PWM_FREQ 1600;

byte temp[1];
byte buff[3];  // position byte, value byte, buffer byte
byte pos;
byte val;

void setup() {

  Serial.begin(SERIAL_BAUDRATE);
  Serial.setTimeout(1);
  Wire.begin();
  
  pwmControllerAll.resetDevices();    // Resets all PCA9685 devices on i2c line

  pwmController1.init();              // Initializes first module using default totem-pole driver mode, and default disabled phase balancer
  pwmController2.init();              // Initializes second module using default totem-pole driver mode, and default disabled phase balancer
  pwmController3.init();

  pwmControllerAll.initAsProxyAddresser(); // Initializes 'fake' module as all-call proxy addresser

  // Enables all-call support to module from 'fake' all-call proxy addresser
  pwmController1.enableAllCallAddress(pwmControllerAll.getI2CAddress());
  pwmController2.enableAllCallAddress(pwmControllerAll.getI2CAddress()); // On both
  pwmController3.enableAllCallAddress(pwmControllerAll.getI2CAddress()); // On both

  for(int i = 0; i < 48; i++){
    if(0 <= i && i < 16){
        pwmController1.setChannelPWM(i, 0);
    } else if (16 <= i && i < 32){
        pwmController2.setChannelPWM(i-16, 0);
    } else if (32 <= i && i < 48){
        pwmController3.setChannelPWM(i-32, 0);
    }
  }
  
  
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB
  }
}

void read_serial_data(){
  Serial.readBytes(temp, 1);
  if (temp[0] == 0){
    Serial.print("error");
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
    } else if (16 <= buff[0] && buff[0] < 32){
        pwmController2.setChannelPWM(buff[0]-16, buff[1] << 4);
    } else if (32 <= buff[0] && buff[0] < 48){
        pwmController3.setChannelPWM(buff[0]-32, buff[1] << 4);
    }
  
  }
}
