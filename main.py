import os
import onnxruntime as ort
import numpy as np
import time
import cv2
import pyautogui
import pytweening
import win32api, win32con, win32gui, win32com
import config
import guest_order
from cooking import get_cooking_info
from process import get_window_position

def handler():
    start = time.time()
    img = cv2.imread('saweima5.png')
    img = cv2.resize(img, (int(img.shape[1] * config.SCALE_FACTOR), int(img.shape[0] * config.SCALE_FACTOR)), interpolation=cv2.INTER_AREA)
    (order_map, img) = guest_order.get_order_info(img)
    order_list = [item for k,v in order_map.items() for item in v['list']]
    print(order_list)
    cooking_order_list, img = get_cooking_info(img)
    end = time.time()
    print("耗时: {:.4f} seconds".format(end - start))
    cv2.imwrite("output.png", img)

if __name__ == '__main__':
    # if get_window_position(config.PROCESS_NAME)[1] is None:
    #     time.sleep(2)
    #     exit(0)

    handler()