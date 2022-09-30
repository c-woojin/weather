from enum import IntEnum, Enum


class WeatherStatus(IntEnum):
    SUNNY = 0
    CLOUDY = 1
    RAINY = 2
    SNOWY = 3


class GreetingMessage(str, Enum):
    HEAVY_SNOW = "폭설이 내리고 있어요."
    SNOW = "눈이 포슬포슬 내립니다."
    HEAVY_RAIN = "폭우가 내리고 있어요."
    RAIN = "비가 오고 있습니다."
    CLOUD = "날씨가 약간은 칙칙해요."
    SUNNY = "따사로 햇살을 맞으세요."
    COLD = "날이 참 춥네요."
    OTHERS = "날씨가 참 맑습니다."
