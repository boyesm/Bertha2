import serial
import struct

arduino = serial.Serial(port='/dev/cu.usbmodem1101', baudrate=500000, timeout=.1)

def change_value(pos=0, value=255):
    if value > 255: value = 255
    arduino.write(struct.pack('>2B', pos, value))