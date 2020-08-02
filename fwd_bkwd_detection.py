import serial
import time
import pyautogui

ser = serial.Serial("/dev/cu.usbmodem141101", 9600)
prev_dist = 45.0


def motion_detection(dist):
    if dist < 40:
        print('MOVE FORWARD and dist is : ' + str(dist))
        return 1
    elif 40 <= dist < 80:
        print('Stay Neutral and dist is :' + str(dist))
        return 0
    elif dist >= 80:
        print('MOVE BACKWARD and dist is :' + str(dist))
        return -1


def get_distance(serial_obj):
    if serial_obj.isOpen:
        val = serial_obj.read_all().decode().split("\r\n")[-4]
        return float(val)
    else:
        # returning value which will keep the player in neutral position
        return 45


def decision(serial_obj, prev_dist):
    try:
        dist = get_distance(serial_obj)
        if dist > 1000:
            raise Exception()
    except Exception:
        return 0, prev_dist
    return motion_detection(dist), dist


while ser.isOpen:
    # time.sleep(0.5)
    flag, prev_dist = decision(ser, prev_dist)
    # ser.close()
    if flag == 1:
        pyautogui.keyUp('left')
        pyautogui.keyDown('right')
        pass
    elif flag == -1:
        pyautogui.keyUp('right')
        pyautogui.keyDown('left')
        pass
    else:
        pyautogui.keyUp('right')
        pyautogui.keyUp('left')
        pass

ser.close()
