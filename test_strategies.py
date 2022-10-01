from typing import Callable, Dict, Tuple, Any

import pytest

from constants import WeatherStatus, GreetingMessage, TemperatureMaxMinMessage, TemperatureDifferenceMessage
from model import DefaultGreetingMessageStrategy, DefaultTemperatureMessageStrategy, Weather


class TestMessageStrategy:
    @pytest.mark.parametrize(
        "weather_condition, expected_message",
        [
            (dict(status=WeatherStatus.SNOWY, precipitation=200.0), GreetingMessage.HEAVY_SNOW),
            (dict(status=WeatherStatus.SNOWY, precipitation=100.0), GreetingMessage.HEAVY_SNOW),
            (dict(status=WeatherStatus.SNOWY, precipitation=100.0, temperature=5.0), GreetingMessage.HEAVY_SNOW),
            (dict(status=WeatherStatus.SNOWY, precipitation=50.0), GreetingMessage.SNOW),
            (dict(status=WeatherStatus.SNOWY, precipitation=50.0, temperature=5.0), GreetingMessage.SNOW),
            (dict(status=WeatherStatus.RAINY, precipitation=200.0), GreetingMessage.HEAVY_RAIN),
            (dict(status=WeatherStatus.RAINY, precipitation=100.0), GreetingMessage.HEAVY_RAIN),
            (dict(status=WeatherStatus.RAINY, precipitation=100.0, temperature=-5.0), GreetingMessage.HEAVY_RAIN),
            (dict(status=WeatherStatus.RAINY, precipitation=50.0), GreetingMessage.RAIN),
            (dict(status=WeatherStatus.RAINY, precipitation=0.0), GreetingMessage.RAIN),
            (dict(status=WeatherStatus.RAINY, precipitation=0.0, temperature=-5.0), GreetingMessage.RAIN),
            (dict(status=WeatherStatus.CLOUDY), GreetingMessage.CLOUD),
            (dict(status=WeatherStatus.CLOUDY, precipitation=10.0), GreetingMessage.CLOUD),
            (dict(status=WeatherStatus.CLOUDY, temperature=10.0), GreetingMessage.CLOUD),
            (dict(status=WeatherStatus.CLOUDY, precipitation=10.0, temperature=10.0), GreetingMessage.CLOUD),
            (dict(status=WeatherStatus.SUNNY, temperature=40.0), GreetingMessage.SUNNY),
            (dict(status=WeatherStatus.SUNNY, temperature=30.0), GreetingMessage.SUNNY),
            (dict(status=WeatherStatus.SUNNY, temperature=30.0, precipitation=10.0), GreetingMessage.SUNNY),
            (dict(temperature=-5.0), GreetingMessage.COLD),
            (dict(temperature=0.0), GreetingMessage.COLD),
            (dict(status=WeatherStatus.SUNNY, temperature=0.0), GreetingMessage.COLD),
            (dict(status=WeatherStatus.SUNNY, temperature=20.0), GreetingMessage.OTHERS),
        ],
    )
    def test_default_greeting_messages(self, weather_condition: Dict, expected_message: str, get_weather: Callable):
        weather = get_weather(
            hour_offset=weather_condition.get("hour_offset"),
            status=weather_condition.get("status"),
            temperature=weather_condition.get("temperature"),
            precipitation=weather_condition.get("precipitation"),
        )
        greeting_message = DefaultGreetingMessageStrategy.generate_message(weather)

        assert greeting_message == expected_message

    @pytest.mark.parametrize(
        "temperatures, expected_message",  # temperatures: (current, -6h, -12h, -18h, -24h)
        [
            (
                (20.0, 21.0, 23.0, 24.0, 25.0),
                f"{TemperatureDifferenceMessage.LESS_HOT.format(difference=5.0)} {TemperatureMaxMinMessage.format(max=25.0, min=20.0)}",
            ),
        ],
    )
    def test_default_temperature_messages(
        self, temperatures: Tuple, expected_message: str, get_weather: Callable[..., Weather]
    ):
        weathers = (
            get_weather(hour_offset=i * -6, temperature=temperature) for i, temperature in enumerate(temperatures)
        )
        temperature_message = DefaultTemperatureMessageStrategy.generate_message(tuple(weathers))

        assert temperature_message == expected_message
