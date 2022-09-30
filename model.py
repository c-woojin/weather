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
        if weather.status == WeatherStatus.SNOWY and weather.precipitation >= 100.0:
            message = GreetingMessage.HEAVY_SNOW
        elif weather.status == WeatherStatus.SNOWY:
            message = GreetingMessage.SNOW
        elif weather.status == WeatherStatus.RAINY and weather.precipitation >= 100.0:
            message = GreetingMessage.HEAVY_RAIN
        elif weather.status == WeatherStatus.RAINY:
            message = GreetingMessage.RAIN
        elif weather.status == WeatherStatus.CLOUDY:
            message = GreetingMessage.CLOUD
        elif weather.status == WeatherStatus.SUNNY and weather.temperature >= 30.0:
            message = GreetingMessage.SUNNY
        elif weather.temperature <= 0.0:
            message = GreetingMessage.COLD
        else:
            message = GreetingMessage.OTHERS

        return message
