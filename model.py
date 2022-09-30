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
        return GreetingMessage.HEAVY_SNOW
