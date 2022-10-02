import datetime
from typing import Callable, Tuple

from weather.domain.message_strategies import (
    AbstractGreetingMessageStrategy,
    AbstractTemperatureMessageStrategy,
    AbstractHeadsUpMessageStrategy,
)
from weather.domain.models import WeatherSummary, Location, Weather, Forecast


class FakeGreetingMessageStrategy(AbstractGreetingMessageStrategy):
    @staticmethod
    def generate_message(weathers: Tuple[Weather, ...]) -> str:
        return "Fake Greeting Message"


class FakeTemperatureMessageStrategy(AbstractTemperatureMessageStrategy):
    @staticmethod
    def generate_message(weathers: Tuple[Weather, ...]) -> str:
        return "Fake Temperature Message"


class FakeHeadsUpMessageStrategy(AbstractHeadsUpMessageStrategy):
    @staticmethod
    def generate_message(weathers: Tuple[Weather, ...]) -> str:
        return "Fake Heads Up Message"


class TestWeatherSummary:
    def test_generate_message(self, get_weather: Callable[..., Weather], get_forecast: Callable[..., Forecast]):
        weather_summary = WeatherSummary(
            location=Location(latitude=127.7, longitude=35.9),
            date_time=datetime.datetime.now(),
            weathers=tuple((get_weather() for _ in range(3))),
            forecasts=tuple((get_forecast() for _ in range(3))),
            greeting_message_strategy=FakeGreetingMessageStrategy,
            temperature_message_strategy=FakeTemperatureMessageStrategy,
            heads_up_message_strategy=FakeHeadsUpMessageStrategy,
        )

        greeting_message = weather_summary.generate_greeting_message()
        temperature_message = weather_summary.generate_temperature_message()
        heads_up_message = weather_summary.generate_heads_up_message()

        assert greeting_message == "Fake Greeting Message"
        assert temperature_message == "Fake Temperature Message"
        assert heads_up_message == "Fake Heads Up Message"
