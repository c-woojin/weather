from typing import Callable, Dict

import pytest

from constants import WeatherStatus, GreetingMessage
from model import DefaultGreetingMessageStrategy


class TestDefaultGreetingMessageStrategy:
    @pytest.mark.parametrize(
        "weather_condition, expected_message",
        [
            (dict(status=WeatherStatus.SNOWY, precipitation=200.0), GreetingMessage.HEAVY_SNOW),
            (dict(status=WeatherStatus.SNOWY, precipitation=100.0), GreetingMessage.HEAVY_SNOW),
            (dict(status=WeatherStatus.SNOWY, precipitation=50.0), GreetingMessage.SNOW),
        ],
    )
    def test_greeting_messages(self, weather_condition: Dict, expected_message: str, get_weather: Callable):
        weather = get_weather(
            hour_offset=weather_condition.get("hour_offset"),
            status=weather_condition.get("status"),
            temperature=weather_condition.get("temperature"),
            precipitation=weather_condition.get("precipitation"),
        )
        greeting_message = DefaultGreetingMessageStrategy.generate_message(weather)

        assert greeting_message == expected_message
