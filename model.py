import abc
import dataclasses
from typing import Tuple, Dict

from constants import WeatherStatus, GreetingMessage, TemperatureDifferenceMessage, TemperatureMaxMinMessage


class InvalidWeatherHourOffset(Exception):
    pass


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


class AbstractTemperatureMessageStrategy(abc.ABC):
    @staticmethod
    def generate_message(weathers: Tuple[Weather]) -> str:
        raise NotImplementedError


class DefaultTemperatureMessageStrategy(AbstractTemperatureMessageStrategy):
    @staticmethod
    def generate_message(weathers: Tuple[Weather]) -> str:
        temperatures_by_hour_offset: Dict[int, float] = {
            weather.hour_offset: weather.temperature for weather in weathers
        }

        current_temperature = temperatures_by_hour_offset.get(0)
        old_temperature = temperatures_by_hour_offset.get(-24)

        if None in (current_temperature, old_temperature):
            raise InvalidWeatherHourOffset("There is no current weather or weather 24 hours ago.")

        difference_message = DefaultTemperatureMessageStrategy._generate_difference_message(
            current_temperature=current_temperature, old_temperature=old_temperature
        )

        max_min_message = DefaultTemperatureMessageStrategy._generate_max_min_message(
            temperatures=tuple((weather.temperature for weather in weathers))
        )

        return f"{difference_message} {max_min_message}"

    @staticmethod
    def _generate_difference_message(current_temperature: float, old_temperature: float) -> str:
        difference = current_temperature - old_temperature

        if current_temperature >= 15.0:
            if difference < 0:
                message = TemperatureDifferenceMessage.LESS_HOT.format(difference=abs(difference))
            elif difference > 0:
                message = TemperatureDifferenceMessage.HOTTER.format(difference=difference)
            else:
                message = TemperatureDifferenceMessage.AS_HOT_AS
        else:
            if difference < 0:
                message = TemperatureDifferenceMessage.COLDER.format(difference=abs(difference))
            elif difference > 0:
                message = TemperatureDifferenceMessage.LESS_COLD.format(difference=difference)
            else:
                message = TemperatureDifferenceMessage.AS_COLD_AS

        return message

    @staticmethod
    def _generate_max_min_message(temperatures: Tuple[float]) -> str:
        return TemperatureMaxMinMessage.format(max=max(temperatures), min=min(temperatures))
