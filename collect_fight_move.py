import cv2
import numpy as np
import os
import time

# Create the directory structure
# punch = 1 , not punch = 0
if not os.path.exists("fight_move_data"):
    os.makedirs("fight_move_data")
    os.makedirs("fight_move_data/train")
    os.makedirs("fight_move_data/test")
    os.makedirs("fight_move_data/train/0")
    os.makedirs("fight_move_data/train/1")
    os.makedirs("fight_move_data/test/0")
    os.makedirs("fight_move_data/test/1")


# Train or test
mode = 'train'
# 1 for capturing punch data, for capturing no punch put it as 0
move_mode = 1
total_move_count = 150

directory = 'fight_move_data/' + mode + '/'

cap = cv2.VideoCapture(0)
cv2.namedWindow("Fight Window")
if move_mode == 1:
    signal = {
        0:"Get Set",
        1:"Punch",
        2:"Pause!"
    }
elif move_mode == 0:
    signal = {
        0: "Get Set",
        1: "Stay",
        2: "Pause!"
    }
# time.sleep(5)
for num in range(total_move_count):
    # Getting count of existing images
    count = {0: len(os.listdir(directory + "/0")),
             1: len(os.listdir(directory + "/1"))}
    count_down = 3
    start = time.time()
    elapsed = 0
    while True:
        elapsed = time.time() - start
        _, frame = cap.read()
        # Simulating mirror image
        frame = cv2.flip(frame, 1)


        # Printing the count in each set to the screen
        cv2.putText(frame, "MODE : " + mode, (10, 50), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 1)
        cv2.putText(frame, "IMAGE COUNT", (10, 100), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 1)
        cv2.putText(frame, "ZERO : " + str(count[0]), (10, 120), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        cv2.putText(frame, "ONE : " + str(count[1]), (10, 150), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        if int(elapsed) in signal:
            cv2.putText(frame, "TIME : " + str(int(elapsed)) + " " + signal[int(elapsed)], (10, 210),
                        cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 2)

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
        roi = cv2.resize(roi, (64, 64))

        cv2.imshow("Frame", frame)

        # _, mask = cv2.threshold(mask, 200, 255, cv2.THRESH_BINARY)
        # kernel = np.ones((1, 1), np.uint8)
        # img = cv2.dilate(mask, kernel, iterations=1)
        # img = cv2.erode(mask, kernel, iterations=1)
        # do the processing after capturing the image!

        roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        # _, roi = cv2.threshold(roi, 50, 255, cv2.THRESH_BINARY)
        cv2.imshow("ROI", roi)

        # capture when count down drops to zero
        if int(elapsed) >= count_down:
            cv2.imwrite(directory + str(move_mode) + '/' + str(count[move_mode]) + '.jpg', roi)
            print("Taken!")
            break

        interrupt = cv2.waitKey(10)
        if interrupt & 0xFF == 27:  # esc key
            break
        # if interrupt & 0xFF == ord('0'):
        #     cv2.imwrite(directory + '0/' + str(count['zero']) + '.jpg', roi)
        # if interrupt & 0xFF == ord('1'):
        #     cv2.imwrite(directory + '1/' + str(count['one']) + '.jpg', roi)
            # if you have captured images up till your desired count then stop

    if total_move_count == count[move_mode]:
        break

cap.release()
cv2.destroyAllWindows()

