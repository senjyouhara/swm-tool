import threading
import time
from typing import List

import cv2
import numpy as np
import pyautogui

import config
import guest_order
from cooking import get_cooking_info
from keyboardUtil import circle_drag_move, click, long_click, drag_move
from model.OrderInfo import OrderInfo
from myenum import OrderTypeEnum
from process import get_window_position
from util import find


class Cuisine:
    order_list: List[OrderInfo] = []
    cooking_order_list: List[OrderInfo] = []
    img = None

    def window_position(self):
        return get_window_position(config.PROCESS_NAME)

    def screen_shot(self):
        # pos, handle = self.window_position()
        # if handle is None:
        #     time.sleep(2)
        #     exit(0)
        # (x1,y1,x2,y2) = pos
        # img = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))
        img = cv2.imread('saweima2.png')
        self.img = np.array(img)
        self.img = cv2.resize(self.img,
                              (int(self.img.shape[1] * config.SCALE_FACTOR), int(self.img.shape[0] * config.SCALE_FACTOR)),
                              interpolation=cv2.INTER_AREA)

    def get_order_list(self):
        start = time.time()
        (order_map, self.img) = guest_order.get_order_info(self.img)
        self.order_list = [item for k, v in order_map.items() for item in v['list']]
        # print(order_list)
        self.cooking_order_list, self.img = get_cooking_info(self.img)
        # print(cooking_order_list)
        end = time.time()
        print("耗时: {:.4f} seconds".format(end - start))

        return self.order_list,self.cooking_order_list,self.img

    # 切肉
    def add_meat(self):
        current = find(lambda x: x.type == OrderTypeEnum.MEAT, self.cooking_order_list)
        knif = find(lambda x: x.type == OrderTypeEnum.KNIFE, self.cooking_order_list)
        if current is not None and knif is not None:
            circle_drag_move(knif, int((current.x + int(current.w * 0.5)) / config.SCALE_FACTOR),
                             int(current.y / config.SCALE_FACTOR),
                             int((current.x + int(current.w * 0.5)) / config.SCALE_FACTOR),
                             int((current.y + current.h) / config.SCALE_FACTOR), 0.1, 10)

    # 添加黄瓜
    def add_cucumber(self):
        current = find(lambda x: x.type == OrderTypeEnum.CUCUMBER, self.cooking_order_list)
        if current is not None:
            click(int(current.centerX / config.SCALE_FACTOR), int(current.centerY / config.SCALE_FACTOR), 0.1,
                          10)

    # 添加奶酪
    def add_cheese(self):
        current = find(lambda x: x.type == OrderTypeEnum.CHEESE, self.cooking_order_list)
        if current is not None:
            click(int(current.centerX / config.SCALE_FACTOR), int(current.centerY / config.SCALE_FACTOR), 0.1,
                          10)

    # 切土豆
    def cut_fries(self):
        current = find(lambda x: x.type == OrderTypeEnum.POTATO, self.cooking_order_list)
        if current is not None:
            long_click(int(current.centerX / config.SCALE_FACTOR), int(current.centerY / config.SCALE_FACTOR), 10)
            def mythread():
                time.sleep(10)
                self.get_order_list()
                self.add_fries()
            threading.Thread(target=mythread).start()


    # 添加薯条
    def add_fries(self):
        current = find(lambda x: x.type == OrderTypeEnum.DEEP_FRYER_FINISHED, self.cooking_order_list)
        if current is not None:
            click(int(current.centerX / config.SCALE_FACTOR), int(current.centerY / config.SCALE_FACTOR), 0.1)

    # 制作沙威玛
    def add_saweima(self):
        pie = find(lambda x: x.type == OrderTypeEnum.PIE, self.cooking_order_list)
        pies = find(lambda x: x.type == OrderTypeEnum.MULTIPLE_PIE, self.cooking_order_list)
        saweima = find(lambda x: x.type == OrderTypeEnum.SAWEIMA_FINISHED, self.cooking_order_list)

        if saweima is not None:
            return

        if pies is None:
            return

        if pie is None:
            click(int(pies.centerX / config.SCALE_FACTOR), int(pies.centerY / config.SCALE_FACTOR), 0.1)
            time.sleep(0.2)
            self.get_order_list()

        tmp_list = [OrderTypeEnum.MEAT_PLATE, OrderTypeEnum.CUCUMBER_PLATE, OrderTypeEnum.CHEESE_PLATE,
                    OrderTypeEnum.FRENCH_FRIES_PLATE, ]
        for type in tmp_list:
            tmp = find(lambda x: x.type == type, self.cooking_order_list)
            click(int(tmp.centerX / config.SCALE_FACTOR), int(tmp.centerY / config.SCALE_FACTOR), 0.1, 3)
            time.sleep(0.2)

        drag_move(int((pie.centerX) / config.SCALE_FACTOR), int((pie.y + pie.h) / config.SCALE_FACTOR),
                  int((pie.centerX) / config.SCALE_FACTOR), int((pie.y) / config.SCALE_FACTOR), 0.1)
        time.sleep(0.2)

    # 打包沙威玛
    def add_package(self):
        package = find(lambda x: x.type == OrderTypeEnum.PACKAGING_BAG, self.cooking_order_list)
        saweima_roll = find(lambda x: x.type == OrderTypeEnum.SAWEIMA_ROLL, self.cooking_order_list)
        if package is None or saweima_roll is None:
            return

        drag_move(int((package.centerX) / config.SCALE_FACTOR), int((package.centerY) / config.SCALE_FACTOR),
                  int((saweima_roll.centerX) / config.SCALE_FACTOR), int((saweima_roll.centerY) / config.SCALE_FACTOR), 0.1)

    def food_for_guest(self, type, guestType):
        food = find(lambda x: x.type == type, self.cooking_order_list)
        if len(self.order_list) > 0:
            current = find(lambda x: x.type == guestType, self.order_list)
            if current is not None:
                drag_move(int((food.centerX) / config.SCALE_FACTOR), int((food.centerY) / config.SCALE_FACTOR),
                  int((current.centerX) / config.SCALE_FACTOR), int((current.centerY) / config.SCALE_FACTOR), 0.1)
                self.order_list.remove(current)

    def change_cook(self):
        current = find(lambda x: x.type == OrderTypeEnum.COOK, self.cooking_order_list)
        if current is not None:
            click(int(current.centerX / config.SCALE_FACTOR), int(current.centerY / config.SCALE_FACTOR), 0.1)

    def exec(self):
        # 计数器  每3次添加一次小料
        counter = 0
        while True:
            self.screen_shot()
            self.get_order_list()

            if counter == 0:
                self.add_meat()
                self.change_cook()
                time.sleep(0.5)
                self.add_cucumber()
                self.add_cheese()
                self.change_cook()
                time.sleep(0.5)
                self.cut_fries()

            self.add_saweima()
            time.sleep(0.5)
            self.food_for_guest(OrderTypeEnum.SAWEIMA_FINISHED, OrderTypeEnum.ORDER_SAWEIMA)

            counter+=1
            if counter == 3:
                counter = 0
            time.sleep(2)
        pass