from typing import List, Tuple

import numpy as np
import time
import cv2
from PIL import Image, ImageDraw, ImageFont

import config
from model.OnnxModel import get_onnx_results
from model.OrderInfo import OrderInfo

def cv2AddChineseText(img: np.ndarray, text: str, position: Tuple[int, int], color: Tuple[int, ...], font_size = 14):
    cv2img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pilimg = Image.fromarray(cv2img)
    # PIL图片上打印汉字
    draw = ImageDraw.Draw(pilimg)  # 图片上打印
    # simsun 宋体
    font = ImageFont.truetype("simsun.ttf", font_size, encoding="utf-8")
    # 位置，文字，颜色==红色，字体引入
    draw.text(position, text, color, font=font)
    bbox = pilimg.getbbox()
    # PIL图片转cv2 图片
    return cv2.cvtColor(np.array(pilimg), cv2.COLOR_RGB2BGR), (bbox[2] - bbox[0], bbox[3] - bbox[1])

def img_handle(img, type, template_img):
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    template = cv2.resize(template_img, (int(template_img.shape[1] * config.SCALE_FACTOR), int(template_img.shape[0] * config.SCALE_FACTOR)),interpolation=cv2.INTER_AREA)
    template = cv2.cvtColor(template, cv2.COLOR_BGR2RGBA)
    template = cv2.cvtColor(template, cv2.COLOR_RGBA2GRAY)

    res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(res)
    (startX, startY) = maxLoc
    endX = startX + template.shape[1]
    endY = startY + template.shape[0]
    if maxVal > 0.8:
        item = OrderInfo(
                type,
                x=startX,
                y=startY,
                w=template.shape[1],
                h=template.shape[0],
                centerX=int(startX + template_img.shape[1] * 0.5),
                centerY=int(startY + template_img.shape[0] * 0.5),
                score=0.85,
            )

        return item

    return None

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
            score=0.85,
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
        # {
        #     "type": "油炸锅(已完成)",
        #     "path": "assets/frying-machine-finish.png",
        # },
        {
            "type": "金币",
            "path": "assets/gold.png",
        },
        {
            "type": "土豆",
            "path": "assets/potato.png",
        },
        {
            "type": "包装袋",
            "path": "assets/wrapping-paper.png",
        },
    ]

    order_list: List[OrderInfo] = []
    origin_img = img

    onnx_info_list = get_onnx_results(config.ONNX_MODEL,  img)
    order_list.extend(onnx_info_list)

    for type in type_list:
        tmp = img_handle(img, type['type'], cv2.imread(type['path']))
        if tmp is not None:
            order_list.append(tmp)
    colors = np.random.uniform(0, 255, size=(len(order_list), 3))

    for index,order in enumerate(order_list):
        color = tuple(map(lambda x: int(x),colors[index]))
        rectangle = np.zeros(origin_img.shape[:2], dtype="uint8")
        rectangle = cv2.cvtColor(rectangle, cv2.COLOR_BGR2RGB)

        textImg = np.zeros(origin_img.shape[:2], dtype="uint8")
        textImg, textinfo = cv2AddChineseText(textImg, order.type, (order.x, order.y - 20), (255,255,255), 16)
        textImg = cv2.cvtColor(textImg, cv2.COLOR_BGR2GRAY)

        cv2.rectangle(rectangle, (order.x, order.y), (order.x + order.w, order.y + order.h),
                      color, 2)
        cv2.rectangle(rectangle, (order.x-1, order.y - 20), (order.x + order.w+1  if order.w+1 > textinfo[0] else order.x + textinfo[0], order.y),
                      color, -1)
        rectangle = cv2.cvtColor(rectangle, cv2.COLOR_RGB2BGR)
        ret, mask = cv2.threshold(textImg, 10, 255, cv2.THRESH_BINARY)
        bitwise_and = cv2.bitwise_and(rectangle,rectangle, mask=cv2.bitwise_not(mask))

        gray_rectangle = cv2.cvtColor(bitwise_and, cv2.COLOR_BGR2GRAY)
        ret2, mask2 = cv2.threshold(gray_rectangle, 10, 255, cv2.THRESH_BINARY)

        img2_bg = cv2.bitwise_and(origin_img, origin_img, mask=cv2.bitwise_not(mask2))
        dist = cv2.add(img2_bg, bitwise_and)
        origin_img = dist
        # cv2.imshow("Circle", dist)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()


    return order_list, origin_img
