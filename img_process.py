import cv2
import os


#
# img=cv2.imread('fight_move_data/train/1/0.jpg')
# cv2.imshow('image',img)
# _, roi = cv2.threshold(img, 50, 255, cv2.THRESH_BINARY)
# cv2.imshow('image',roi)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

def process_img(img_path, target_path):
    img = cv2.imread(img_path)
    _, roi = cv2.threshold(img, 50, 255, cv2.THRESH_BINARY)
    cv2.imwrite(target_path, roi)


if not os.path.exists("fight_move_data_p"):
    os.makedirs("fight_move_data_p")
    os.makedirs("fight_move_data_p/train_p")
    os.makedirs("fight_move_data_p/test_p")
    os.makedirs("fight_move_data_p/train_p/0")
    os.makedirs("fight_move_data_p/train_p/1")
    os.makedirs("fight_move_data_p/test_p/0")
    os.makedirs("fight_move_data_p/test_p/1")

# process train imgs
# class_mode = '1'
# mode = 'train_p'
# class_mode = '1'
# mode = 'test_p'
# class_mode = '0'
# mode = 'train_p'
class_mode = '0'
mode = 'test_p'

root = "fight_move_data_p"
actual_path = os.path.join(root.strip("_p"),mode.strip("_p"),class_mode)
for file in os.listdir(actual_path):
    img_path = os.path.join(actual_path,file)
    target_path = os.path.join(root,mode,class_mode,file)
    process_img(img_path, target_path)