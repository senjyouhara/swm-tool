from enum import Enum, unique


@unique
class OrderTypeEnum(Enum):
    COOK = "厨子",
    MEAT = "肉块",
    KNIFE = "小刀",
    POTATO = "土豆",
    POTATO_PROCESS = "土豆(切)",
    MEAT_PLATE = "肉盘",
    CUCUMBER_PLATE = "黄瓜盘",
    CHEESE_PLATE = "奶酪盘",
    FRENCH_FRIES_PLATE = "薯条盘",
    CHEESE = "奶酪",
    CUCUMBER = "黄瓜",
    MULTIPLE_PIE = "大饼(多个)",
    PIE = "大饼",
    PIE_FINISH = "大饼(加好料)",
    SAWEIMA_FINISHED = "沙威玛(已完成)",
    GOLD = "金币",
    PACKAGING_BAG = "包装袋",
    KETCHUP = "番茄酱",
    DEEP_FRYER = "油炸锅",
    DEEP_FRYER_PROCESS = "油炸锅(处理中)",
    DEEP_FRYER_FINISHED = "油炸锅(完成)",
    ORDER_SAWEIMA = "沙威玛",
    ORDER_COLA = "可乐",
    ORDER_ORANGE_JUICE = "橙汁",
    ORDER_JUICE = "果汁",
    ORDER_FRIES = "薯条",
    ORDER_SWEET_POTATO = "红薯",

