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
from keyboardUtil import circle_drag_move, move_to_click, long_click, drag_move
from myenum import OrderTypeEnum
from process import get_window_position
from util import find


def add_meat(cooking_order_list):
    current = find(lambda x: x.type == OrderTypeEnum.MEAT, cooking_order_list)
    knif = find(lambda x: x.type == OrderTypeEnum.KNIFE, cooking_order_list)
    if current is not None and knif is not None:
        circle_drag_move(knif, int((current.x + int(current.w * 0.5)) / config.SCALE_FACTOR),
                         int(current.y / config.SCALE_FACTOR),
                         int((current.x + int(current.w * 0.5)) / config.SCALE_FACTOR),
                         int((current.y + current.h) / config.SCALE_FACTOR), 0.1, 10)

def add_cucumber(cooking_order_list):
    current = find(lambda x: x.type == OrderTypeEnum.CUCUMBER, cooking_order_list)
    if current is not None:
        move_to_click(int(current.centerX / config.SCALE_FACTOR), int(current.centerY / config.SCALE_FACTOR), 0.1, 10)

def add_cheese(cooking_order_list):
    current = find(lambda x: x.type == OrderTypeEnum.CHEESE, cooking_order_list)
    if current is not None:
        move_to_click(int(current.centerX / config.SCALE_FACTOR), int(current.centerY / config.SCALE_FACTOR), 0.1, 10)

def cut_fries(cooking_order_list):
    current = find(lambda x: x.type == OrderTypeEnum.POTATO, cooking_order_list)
    if current is not None:
        long_click(int(current.centerX / config.SCALE_FACTOR), int(current.centerY / config.SCALE_FACTOR), 6)

def add_fries(cooking_order_list):
    current = find(lambda x: x.type == OrderTypeEnum.DEEP_FRYER_FINISHED, cooking_order_list)
    if current is not None:
        move_to_click(int(current.centerX / config.SCALE_FACTOR), int(current.centerY / config.SCALE_FACTOR), 0.1)

def add_saweima(cooking_order_list):
    pie = find(lambda x: x.type == OrderTypeEnum.PIE, cooking_order_list)
    pies = find(lambda x: x.type == OrderTypeEnum.MULTIPLE_PIE, cooking_order_list)

    if pies is None:
        return

    if pie is None:
        move_to_click(int(pies.centerX / config.SCALE_FACTOR), int(pies.centerY / config.SCALE_FACTOR), 0.1)
        time.sleep(0.2)

    tmp_list = [OrderTypeEnum.MEAT_PLATE, OrderTypeEnum.CUCUMBER_PLATE, OrderTypeEnum.CHEESE_PLATE, OrderTypeEnum.FRENCH_FRIES_PLATE, ]
    for type in tmp_list:
        tmp = find(lambda x: x.type == type, cooking_order_list)
        move_to_click(int(tmp.centerX / config.SCALE_FACTOR), int(tmp.centerY / config.SCALE_FACTOR), 0.1, 3)
        time.sleep(0.2)

    drag_move(int((pie.centerX) / config.SCALE_FACTOR), int((pie.y+pie.h) / config.SCALE_FACTOR), int((pie.centerX) / config.SCALE_FACTOR), int((pie.y) / config.SCALE_FACTOR), 0.1)
    time.sleep(0.2)

def add_package(cooking_order_list):
    package = find(lambda x: x.type == OrderTypeEnum.PACKAGING_BAG, cooking_order_list)
    pie = find(lambda x: x.type == OrderTypeEnum.PIE, cooking_order_list)
    if package is None or pie is None:
        return

    drag_move(int((package.centerX) / config.SCALE_FACTOR), int((package.centerY) / config.SCALE_FACTOR),
              int((pie.centerX) / config.SCALE_FACTOR), int((pie.centerY) / config.SCALE_FACTOR), 0.1)


def handler():
    start = time.time()
    # img = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))
    img = cv2.imread('saweima2.png')
    img = cv2.resize(img, (int(img.shape[1] * config.SCALE_FACTOR), int(img.shape[0] * config.SCALE_FACTOR)), interpolation=cv2.INTER_AREA)
    (order_map, img) = guest_order.get_order_info(img)
    order_list = [item for k,v in order_map.items() for item in v['list']]
    # print(order_list)
    cooking_order_list, img = get_cooking_info(img)
    # print(cooking_order_list)
    end = time.time()
    print("耗时: {:.4f} seconds".format(end - start))

    if len(order_list) > 0:
        pass
    else:
        add_meat(cooking_order_list)
        add_cucumber(cooking_order_list)
        add_cheese(cooking_order_list)
        cut_fries(cooking_order_list)
        time.sleep(10)
        add_fries(cooking_order_list)
        # add_saweima(cooking_order_list)
        # time.sleep(0.2)
        # add_package(cooking_order_list)
        pass
    cv2.imwrite("output.png", img)

if __name__ == '__main__':
    # if get_window_position(config.PROCESS_NAME)[1] is None:
    #     time.sleep(2)
    #     exit(0)

    handler()