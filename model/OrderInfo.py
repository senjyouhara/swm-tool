from myenum import OrderTypeEnum


class OrderInfo:
    type: OrderTypeEnum
    x: int
    y: int
    w: int
    h: int
    centerX: int
    centerY: int
    is_finished: bool
    score: float

    def __init__(self, type: OrderTypeEnum, x, y, w, h, centerX, centerY, score, is_finished=False):
        self.type = type
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.score = score
        self.centerX = centerX
        self.centerY = centerY
        self.is_finished = is_finished

    def __str__(self):
        return f'{{type: {self.type}, x: {self.x}, y: {self.y}, w: {self.w}, h {self.h} }}'


