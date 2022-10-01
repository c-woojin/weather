import dataclasses

from src.domain.constants import WeatherStatus


@dataclasses.dataclass(frozen=True)
class Weather:
    hour_offset: int
    status: WeatherStatus
    temperature: float
    precipitation: float


@dataclasses.dataclass(frozen=True)
class Forecast:
    hour_offset: int
    status: WeatherStatus