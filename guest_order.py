import numpy as np
import time
import cv2
from typing import List, Dict

import config
from model.OrderInfo import OrderInfo


def img_handle(img, type, template_img):
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    template = cv2.resize(template_img, (int(template_img.shape[1] * config.SCALE_FACTOR), int(template_img.shape[0] * config.SCALE_FACTOR)),interpolation=cv2.INTER_AREA)
    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    # 取匹配程度大于90%的坐标
    value = np.where(res >= 0.8)
    my_list: List[OrderInfo] = []
    for i in zip(*value[::-1]):  # *代表可选参数
        item = OrderInfo(
            type,
            x=int(int(i[0])),
            y=int(int(i[1])),
            w=int(template_img.shape[1] * config.SCALE_FACTOR),
            h=int(template_img.shape[0] * config.SCALE_FACTOR),
            centerX=int(i[0]) + int(template_img.shape[1]),
            centerY=int(i[1]) + int(template_img.shape[0]),
        )
        my_list.append(item)
    return my_list

def get_order_info(img):

    type_list = [
        {
            "type": "沙威玛",
            "path": "assets/guest_order/swm.png",
        },
        {
            "type": "可乐",
            "path": "assets/guest_order/cola_b.png",
        },
        {
            "type": "橙汁",
            "path": "assets/guest_order/cola_o.png",
        },
        {
            "type": "果汁",
            "path": "assets/guest_order/box.png",
        },
        {
            "type": "薯条",
            "path": "assets/guest_order/shutiao.png",
        },
        {
            "type": "红薯",
            "path": "assets/guest_order/digua.png",
        },
    ]

    order_list: List[OrderInfo] = []
    order_map: Dict[str, Dict[str, List[OrderInfo] ]] = {}

    origin_img = img

    for type in type_list:
        tmp_list = img_handle(img, type['type'], cv2.imread(type['path']))
        order_list.extend(tmp_list)

    order_list.sort(key=lambda x: x.x * 100000 + x.y)
    index = 1
    guest = f"guest {index}"
    prev_order = None
    # origin_img = cv2.cvtColor(origin_img, cv2.COLOR_BGR2RGB)

    for order in order_list:
        cv2.rectangle(origin_img, (order.x, order.y), (order.x + order.w, order.y + order.h),
                      (0, 0, 255), 2)
        if prev_order is not None and (order.x - prev_order.x > 20):
            index += 1
            guest = f"guest {index}"
        if order_map.get(guest) is None:
            order_map[guest] = {
                "list": [],
            }
        order_map[guest]['list'].append(order)
        prev_order = order

    # origin_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    for e in order_map:
        order_map[e]['list'].sort(key=lambda x: x.y * 100000 + x.x)

    return order_map, origin_img