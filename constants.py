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
    SUNNY = "따사로운 햇살을 맞으세요."
    COLD = "날이 참 춥네요."
    OTHERS = "날씨가 참 맑습니다."


class TemperatureDifferenceMessage(str, Enum):
    HOTTER = "어제보다 {difference}도 더 덥습니다."
    COLDER = "어제보다 {difference}도 더 춥습니다."
    LESS_HOT = "어제보다 {difference}도 덜 덥습니다."
    LESS_COLD = "어제보다 {difference}도 덜 춥습니다."
    AS_HOT_AS = "어제와 비슷하게 덥습니다."
    AS_COLD_AS = "어제와 비슷하게 춥습니다."


TemperatureMaxMinMessage = "최고기온은 {max}도, 최저기온은 {min}도 입니다."


class HeadsUpMessage(str, Enum):
    HEAVY_SNOW = "내일 폭설이 내릴 수도 있으니 외출 시 주의하세요."
    SNOWY = "눈이 내릴 예정이니 외출 시 주의하세요."
    HEAVY_RAIN = "폭우가 내릴 예정이에요. 우산을 미리 챙겨 두세요."
    RAIN = "며칠동안 비 소식이 있어요."
    OTHERS = "날씨는 대체로 평온할 예정이에요."
