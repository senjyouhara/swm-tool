from enum import Enum, unique


@unique
class OrderTypeEnum(Enum):
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
    GOLD = "金币",
    PACKAGING_BAG = "包装袋",
    KETCHUP = "番茄酱",
    COOK = "厨子",
    DEEP_FRYER = "油炸锅",
    DEEP_FRYER_FINISHED = "油炸锅(完成)",

