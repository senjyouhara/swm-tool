class OrderInfo:
    type: str
    x: int
    y: int
    w: int
    h: int
    centerX: int
    centerY: int

    def __init__(self, type, x, y, w, h, centerX, centerY):
        self.type = type
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.centerX = centerX
        self.centerY = centerY

    def __str__(self):
        return f'{{type: {self.type}, x: {self.x}, y: {self.y}, w: {self.w}, h {self.h} }}'


