import abc
from typing import Tuple, Dict

from src.domain.constants import WeatherStatus, GreetingMessage, TemperatureDifferenceMessage, TemperatureMaxMinMessage, \
    HeadsUpMessage
from src.domain.models import Weather, Forecast
from src.domain.errors import InvalidWeatherHourOffset


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


class AbstractHeadsUpMessageStrategy(abc.ABC):
    @staticmethod
    def generate_message(forecasts: Tuple[Forecast]) -> str:
        raise NotImplementedError


class DefaultHeadsUpMessageStrategy(AbstractHeadsUpMessageStrategy):
    @staticmethod
    def generate_message(forecasts: Tuple[Forecast]) -> str:
        snow_for_24h = (f for f in forecasts if f.status == WeatherStatus.SNOWY and f.hour_offset <= 24)
        snow_for_48h = (f for f in forecasts if f.status == WeatherStatus.SNOWY and f.hour_offset <= 48)
        rain_for_24h = (f for f in forecasts if f.status == WeatherStatus.RAINY and f.hour_offset <= 24)
        rain_for_48h = (f for f in forecasts if f.status == WeatherStatus.RAINY and f.hour_offset <= 48)

        if len(tuple(snow_for_24h)) >= 2:
            return HeadsUpMessage.HEAVY_SNOW
        elif len(tuple(snow_for_48h)) >= 2:
            return HeadsUpMessage.SNOWY
        elif len(tuple(rain_for_24h)) >= 2:
            return HeadsUpMessage.HEAVY_RAIN
        elif len(tuple(rain_for_48h)) >= 2:
            return HeadsUpMessage.RAIN
        else:
            return HeadsUpMessage.OTHERS