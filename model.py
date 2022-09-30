import abc
import dataclasses

from constants import WeatherStatus


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
        return "폭설이 내리고 있어요."
