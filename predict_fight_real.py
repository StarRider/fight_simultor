import numpy as np
from keras.models import model_from_json
import operator
import cv2
import sys, os
import pyautogui
import serial


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
        b = serial_obj.readline()
        flt = b.decode()
        serial_obj.reset_input_buffer()
        return float(flt)
    else:
        # returning value which will keep the player in neutral position
        return 45


def decision(serial_obj, prev_dist):
    try:
        dist = get_distance(serial_obj)
        if dist > 2000:
            raise Exception()
    except Exception:
        return motion_detection(prev_dist), prev_dist
    return motion_detection(dist), dist


# Loading the model
json_file = open("model-fight.json", "r")
model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(model_json)
# load weights into new model
loaded_model.load_weights("model-fight.h5")
print("Loaded model from disk")

cap = cv2.VideoCapture(0)

# Category dictionary
categories = {0: 'ZERO', 1: 'ONE'}
# ser = serial.Serial("/dev/cu.usbmodem141101", 9600)

notSatisfied = True
while notSatisfied:
    get_mouse_x, get_mouse_y = pyautogui.position()
    print(get_mouse_x,",", get_mouse_y)
    question = input("Are you satified? (y/n)")
    if question == "y":
        notSatisfied = False

pyautogui.moveTo(get_mouse_x, get_mouse_y)
pyautogui.click()
while True:
    _, frame = cap.read()
    # Simulating mirror image
    frame = cv2.flip(frame, 1)

    # Got this from collect-data.py
    # Coordinates of the ROI
    x1 = int(0.2 * frame.shape[1])
    y1 = 10
    x2 = frame.shape[1] - 10
    y2 = int(0.5 * frame.shape[1])
    # Drawing the ROI
    # The increment/decrement by 1 is to compensate for the bounding box
    cv2.rectangle(frame, (x1 - 1, y1 - 1), (x2 + 1, y2 + 1), (255, 0, 0), 1)
    # Extracting the ROI
    roi = frame[y1:y2, x1:x2]

    # Resizing the ROI so it can be fed to the model for prediction
    roi = cv2.resize(roi, (64, 64))
    roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    test_image = roi
    # _, test_image = cv2.threshold(roi, 50, 255, cv2.THRESH_BINARY)
    cv2.imshow("test", test_image)
    # Batch of 1
    result = loaded_model.predict(test_image.reshape(1, 64, 64, 1))

    # check
    prediction = 'Punch' if result[0][0] >= 0.5 else 'Not Punch'
    # prediction = {'ZERO': result[0][0],
    #               'ONE': result[0][1]}
    # # Sorting based on top prediction
    # prediction = sorted(prediction.items(), key=operator.itemgetter(1), reverse=True)
    #
    # # Displaying the predictions
    cv2.putText(frame, prediction, (10, 120), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 2)

    # flag for forward/backward/neutral
    # fwd_ntrl_bkwd_motion_flag, prev_dist = decision(ser, prev_dist)

    # keyboard simulation
    # x=514, y=471

    if prediction == "Punch":
        pyautogui.press('z')
        print("Punch detected!")

    # print("Distance:", prev_dist)
    # print("_____________________________")
    cv2.imshow("Frame", frame)

    interrupt = cv2.waitKey(10)
    if interrupt & 0xFF == 27:  # esc key
        break

# ser.close()
cap.release()
cv2.destroyAllWindows()