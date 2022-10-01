from __future__ import annotations

import dataclasses
from datetime import datetime
from typing import Tuple, Type, TYPE_CHECKING

from src.domain.constants import WeatherStatus

if TYPE_CHECKING:
    from src.domain.message_strategies import (
        AbstractGreetingMessageStrategy,
        AbstractTemperatureMessageStrategy,
        AbstractHeadsUpMessageStrategy,
    )


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


@dataclasses.dataclass(frozen=True)
class Location:
    latitude: float
    longitude: float


@dataclasses.dataclass
class WeatherSummary:
    location: Location
    date_time: datetime
    weathers: Tuple[Weather, ...]
    forecasts: Tuple[Forecast, ...]
    greeting_message_strategy: Type[AbstractGreetingMessageStrategy]
    temperature_message_strategy: Type[AbstractTemperatureMessageStrategy]
    heads_up_message_strategy: Type[AbstractHeadsUpMessageStrategy]

    def generate_greeting_message(self) -> str:
        return self.greeting_message_strategy.generate_message(self.weathers)

    def generate_temperature_message(self) -> str:
        return self.temperature_message_strategy.generate_message(self.weathers)

    def generate_heads_up_message(self) -> str:
        return self.heads_up_message_strategy.generate_message(self.forecasts)
