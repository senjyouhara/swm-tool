from typing import List

import numpy as np
import time
import cv2

import config
from model.OrderInfo import OrderInfo


def img_handle(img, type, template_img):
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    template = cv2.resize(template_img, (int(template_img.shape[1] * config.SCALE_FACTOR), int(template_img.shape[0] * config.SCALE_FACTOR)),interpolation=cv2.INTER_AREA)
    template = cv2.cvtColor(template, cv2.COLOR_BGR2RGBA)
    template = cv2.cvtColor(template, cv2.COLOR_RGBA2GRAY)

    res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)

    my_list = []

    # 取匹配程度大于90%的坐标
    value = np.where(res >= 0.8)
    for i in zip(*value[::-1]):  # *代表可选参数
        item = OrderInfo(
            type,
            x=int(int(i[0])),
            y=int(int(i[1])),
            w=int(template_img.shape[1] * config.SCALE_FACTOR),
            h=int(template_img.shape[0] * config.SCALE_FACTOR),
            centerX=int(i[0]) + int(template_img.shape[1]),
            centerY=int(i[1]) + int(template_img.shape[0]),
            is_finished = False,
        )
        my_list.append(item)
    return my_list[0] if len(my_list) else None

def get_cooking_info(img):
    type_list = [
        # {
        #     "type": "厨子",
        #     "path": "assets/worker.png",
        # },
        {
            "type": "奶酪",
            "path": "assets/cheese.png",
        },
        {
            "type": "黄瓜",
            "path": "assets/cucumber.png",
        },
        {
            "type": "大饼(多个)",
            "path": "assets/flatbread.png",
        },
        {
            "type": "大饼",
            "path": "assets/flatbread-single.png",
        },
        {
            "type": "油炸锅",
            "path": "assets/frying-machine.png",
        },
        {
            "type": "油炸锅(已完成)",
            "path": "assets/frying-machine-finish.png",
        },
        {
            "type": "金币",
            "path": "assets/gold.png",
        },
        {
            "type": "刀",
            "path": "assets/knife.png",
        },
        {
            "type": "肉块",
            "path": "assets/meat.png",
        },
        {
            "type": "土豆",
            "path": "assets/potato.png",
        },
        {
            "type": "土豆(处理中)",
            "path": "assets/potato-process.png",
        },
        {
            "type": "包装袋",
            "path": "assets/wrapping-paper.png",
        },
    ]

    order_list: List[OrderInfo] = []

    origin_img = img

    for type in type_list:
        tmp = img_handle(img, type['type'], cv2.imread(type['path']))
        if tmp is not None:
            order_list.append(tmp)

    for order in order_list:
        cv2.rectangle(origin_img, (order.x, order.y), (order.x + order.w, order.y + order.h),
                      (0, 0, 255), 2)

    return order_list, img

    pass