import abc
import dataclasses

from constants import WeatherStatus, GreetingMessage


@dataclasses.dataclass(frozen=True)
class Weather:
    hour_offset: int
    status: WeatherStatus
    temperature: float
    precipitation: float


class AbstractGreetingMessageStrategy(abc.ABC):
    @staticmethod
    def generate_message(weather: Weather) -> str:
        raise NotImplementedError


class DefaultGreetingMessageStrategy(AbstractGreetingMessageStrategy):
    @staticmethod
    def generate_message(weather: Weather) -> str:
        message = GreetingMessage.OTHERS

        if weather.status == WeatherStatus.SNOWY and weather.precipitation >= 100.0:
            message = GreetingMessage.HEAVY_SNOW
        elif weather.status == WeatherStatus.SNOWY:
            message = GreetingMessage.SNOW

        return message
