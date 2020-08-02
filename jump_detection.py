import serial
import time
import pyautogui
# command to see the serial data via phone
# screen /dev/tty.Bluetooth-Incoming-Port 9600
ser = serial.Serial("/dev/tty.Bluetooth-Incoming-Port", 9600)

while ser.isOpen:
    # time.sleep(0.5)
    print(ser.readline())

ser.close()
