import os
from typing import List

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
from cuisine import Cuisine
from keyboardUtil import circle_drag_move, long_click, drag_move
from model.OrderInfo import OrderInfo
from myenum import OrderTypeEnum
from process import get_window_position
from util import find

def handler():
    curses = Cuisine()
    curses.screen_shot()
    curses.get_order_list()
    cv2.imwrite("output.png", curses.img)

if __name__ == '__main__':
    handler()