import pyautogui
import pytweening

from model.OrderInfo import OrderInfo


# 移动到指定地方并点击
def click(x: int, y: int, timeout: float, circle_count=1):
    pyautogui.moveTo(x, y, timeout, pytweening.easeOutQuad)  # 相对于当前位置移动鼠标，x、y可以为负数
    pyautogui.click(x=x, y=y, clicks=circle_count)  # 左击当前位置

# 循环拖拽移动
def circle_drag_move(orderInfo: OrderInfo,x: int, y: int, endx: int, endy: int, timeout: float, circle_count: int):
    pyautogui.moveTo(orderInfo.centerX, orderInfo.centerY, timeout, pytweening.easeOutQuad)
    pyautogui.dragTo(x=x, y=y, duration=timeout, button='left')
    for i in range(circle_count):
        pyautogui.dragTo(x=endx, y=endy, duration=timeout, button='left')
        pyautogui.dragTo(x=x, y=y, duration=timeout, button='left')


# 拖拽物体到指定地方
def drag_move(x: int, y: int, targetX: int, targetY: int, timeout: float):
    pyautogui.moveTo(x, y, timeout, pytweening.easeOutQuad)
    pyautogui.dragTo(x=x, y=y, duration=timeout, button='left')
    pyautogui.dragTo(x=targetX, y=targetY, duration=timeout, button='left')


# 长按
def long_click(x: int, y: int, timeout: float):
    pyautogui.moveTo(x, y, 0.1, pytweening.easeOutQuad)
    pyautogui.click(x=x, y=y, duration=timeout)  # 左击当前位置

