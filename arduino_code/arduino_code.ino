#include "PCA9685.h"

#define NUMBER_OF_CHANNELS 50
#define I2C_FREQ 115200
#define SERIAL_BAUDRATE 115200
#define PWM_FREQ 1600

PCA9685 pwmController1(B000000);
PCA9685 pwmController2(B000001);
PCA9685 pwmController3(B000010);

// Not a real device, will act as a proxy to pwmController1 and pwmController2, using all-call i2c address 0xE0, and default Wire @400kHz
PCA9685 pwmControllerAll(PCA9685_I2C_DEF_ALLCALL_PROXYADR);

byte temp[1];
byte buff[3];  // position byte, value byte, buffer byte
byte pos;
byte val;


// TODO: Make sure that cur_time can be handled as a super big number. It gets really big. long long int is 25 days of milliseconds. works just fine.

long long int on_at[50] = {0}; // when each value was turned on last in ms. if off, value is 0
long long int cur_time = 0;


void read_serial_data(){
  Serial.readBytes(temp, 1);
  if (temp[0] == 0){
    Serial.println("error");
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


void change_channel_value(int channel, int value){
  if(0 <= channel && channel < 16){
      pwmController1.setChannelPWM(channel, value << 4);
  } else if (16 <= channel && channel < 32){
      pwmController2.setChannelPWM(channel-16, value << 4);
  } else if (32 <= channel && channel < 48){
      pwmController3.setChannelPWM(channel-32, value << 4);
  }
  return;
}


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

  // set all solenoids to 0
  for(int i = 0; i < 48; i++){
    change_channel_value(i, 0);
  }
  
  
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB
  }

//  delay(5000);
  

//  Serial.println("on_at:");
  for(int i = 0; i < NUMBER_OF_CHANNELS; i++){
//    Serial.print(on_at[i]);
//    Serial.print(", ");
  }
}



void loop() {

  // get current time
  // create array where each index corresponds with a pwm channel and the value is when the signal was turned on
  cur_time = millis();

  // this code will shut off any solenoids that have been on for too long.
//  Serial.print("Solenoids have been on for: ");
  for(int i = 0; i < NUMBER_OF_CHANNELS; i++){
    if(on_at[i] == 0){
//      Serial.print(on_at[i]);
//      Serial.print(", ");
    } else if (cur_time - on_at[i] > 1000) {  // if solenoid is on for more than (.)5 seconds
//      Serial.println("ON FOR TOO LONG");
      on_at[i] = 0;
      change_channel_value(i, 0);
//      Serial.print(on_at[i]);
//      Serial.print(", "); 
    } else {
//      Serial.print(cur_time - on_at[i]);
//      Serial.print(", ");
    }
  }
//  Serial.println();
  ////////

  if (Serial.available() > 0) {

//    Serial.println("Reading serial data here!");

    read_serial_data();
    buff[0] = temp[0];  // channel
    read_serial_data();
    buff[1] = temp[0];  // value to set
    read_end_byte();
    buff[2] = temp[0];

//    Serial.print(buff[0]);
//    Serial.print(" ");
//    Serial.print(buff[1]);
//    Serial.print(" ");
//    Serial.print(buff[2]);
//    Serial.print('\n');
    
    buff[0] -= 1;
    buff[1] -= 1;


    // this code will set an array value for the time the solenoid turned on    
    if(buff[1] != 0 && on_at[buff[0]] == 0){  // if setting to a non-zero value and ...
//      Serial.print("Set " + String(buff[0]) + " to ");
//      Serial.println(cur_time);
      on_at[buff[0]] = cur_time;
    } else {
//      Serial.println("Set " + String(buff[0]) + " to zero.");
      on_at[buff[0]] = 0;
    }
    //////////
    
    
    change_channel_value(buff[0], buff[1]);
  
  }
}
