from typing import Callable, Dict, Tuple

import pytest

from src.domain.constants import (
    WeatherStatus,
    GreetingMessage,
    TemperatureMaxMinMessage,
    TemperatureDifferenceMessage,
    HeadsUpMessage,
)
from src.domain.errors import InvalidWeatherHourOffset
from src.domain.models import Weather, Forecast
from src.domain.message_strategies import (
    DefaultGreetingMessageStrategy,
    DefaultTemperatureMessageStrategy,
    DefaultHeadsUpMessageStrategy,
)


class TestDefaultGreetingMessageStrategy:
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
    def test_generate_message(
        self, weather_condition: Dict, expected_message: str, get_weather: Callable[..., Weather]
    ):
        current_weather = get_weather(
            hour_offset=0,
            status=weather_condition.get("status"),
            temperature=weather_condition.get("temperature"),
            precipitation=weather_condition.get("precipitation"),
        )
        weathers = (current_weather, get_weather(hour_offset=-6), get_weather(hour_offset=12))
        greeting_message = DefaultGreetingMessageStrategy.generate_message(weathers)

        assert greeting_message == expected_message

    def test_raise_invalid_weather_hour_offset_error_when_not_given_current_weather(
        self, get_weather: Callable[..., Weather]
    ):
        weathers = (get_weather(hour_offset=-6), get_weather(hour_offset=-12), get_weather(hour_offset=-18))

        with pytest.raises(InvalidWeatherHourOffset):
            DefaultGreetingMessageStrategy.generate_message(weathers)


class TestDefaultTemperatureMessageStrategy:
    @pytest.mark.parametrize(
        "temperatures, expected_message",  # temperatures: (current, -6h, -12h, -18h, -24h)
        [
            (
                (20.0, 21.0, 23.0, 24.0, 25.0),
                f"{TemperatureDifferenceMessage.LESS_HOT.format(difference=5.0)} {TemperatureMaxMinMessage.format(max=25.0, min=20.0)}",  # noqa: E501
            ),
            (
                (15.0, 21.0, 23.0, 24.0, 25.0),
                f"{TemperatureDifferenceMessage.LESS_HOT.format(difference=10.0)} {TemperatureMaxMinMessage.format(max=25.0, min=15.0)}",  # noqa: E501
            ),
            (
                (10.0, 21.0, 23.0, 24.0, 25.0),
                f"{TemperatureDifferenceMessage.COLDER.format(difference=15.0)} {TemperatureMaxMinMessage.format(max=25.0, min=10.0)}",  # noqa: E501
            ),
            (
                (20.0, 21.0, 23.0, 24.0, 15.0),
                f"{TemperatureDifferenceMessage.HOTTER.format(difference=5.0)} {TemperatureMaxMinMessage.format(max=24.0, min=15.0)}",  # noqa: E501
            ),
            (
                (15.0, 21.0, 23.0, 24.0, 10.0),
                f"{TemperatureDifferenceMessage.HOTTER.format(difference=5.0)} {TemperatureMaxMinMessage.format(max=24.0, min=10.0)}",  # noqa: E501
            ),
            (
                (10.0, 9.0, 11.0, 3.0, 5.0),
                f"{TemperatureDifferenceMessage.LESS_COLD.format(difference=5.0)} {TemperatureMaxMinMessage.format(max=11.0, min=3.0)}",  # noqa: E501
            ),
            (
                (20.0, 15.0, 11.0, 22.0, 20.0),
                f"{TemperatureDifferenceMessage.AS_HOT_AS} {TemperatureMaxMinMessage.format(max=22.0, min=11.0)}",
            ),
            (
                (15.0, 15.0, 11.0, 22.0, 15.0),
                f"{TemperatureDifferenceMessage.AS_HOT_AS} {TemperatureMaxMinMessage.format(max=22.0, min=11.0)}",
            ),
            (
                (10.0, 15.0, 11.0, 22.0, 10.0),
                f"{TemperatureDifferenceMessage.AS_COLD_AS} {TemperatureMaxMinMessage.format(max=22.0, min=10.0)}",
            ),
        ],
    )
    def test_generate_message(self, temperatures: Tuple, expected_message: str, get_weather: Callable[..., Weather]):
        weathers = (
            get_weather(hour_offset=i * -6, temperature=temperature) for i, temperature in enumerate(temperatures)
        )
        temperature_message = DefaultTemperatureMessageStrategy.generate_message(tuple(weathers))

        assert temperature_message == expected_message

    def test_raise_invalid_weather_hour_offset_error_when_not_given_current_weather(
        self, get_weather: Callable[..., Weather]
    ):
        weathers = (
            get_weather(hour_offset=-6),
            get_weather(hour_offset=-12),
            get_weather(hour_offset=-18),
            get_weather(hour_offset=-24),
        )

        with pytest.raises(InvalidWeatherHourOffset):
            DefaultTemperatureMessageStrategy.generate_message(weathers)

    def test_raise_invalid_weather_hour_offset_error_when_not_given_weather_before_24h(
        self, get_weather: Callable[..., Weather]
    ):
        weathers = (
            get_weather(hour_offset=-0),
            get_weather(hour_offset=-6),
            get_weather(hour_offset=-12),
            get_weather(hour_offset=-18),
        )

        with pytest.raises(InvalidWeatherHourOffset):
            DefaultTemperatureMessageStrategy.generate_message(weathers)


class TestDefaultHeadsUpMessageStrategy:
    @pytest.mark.parametrize(
        "weather_statuses, expected_message",  # weather_statuses: (+6h, +12h, +18h, +24h, +30h, +36h, +42h, +48h)
        [
            (
                (
                    WeatherStatus.SNOWY,
                    WeatherStatus.RAINY,
                    WeatherStatus.SNOWY,
                    WeatherStatus.RAINY,
                    WeatherStatus.SUNNY,
                    WeatherStatus.SUNNY,
                    WeatherStatus.CLOUDY,
                    WeatherStatus.CLOUDY,
                ),
                HeadsUpMessage.HEAVY_SNOW,
            ),
            (
                (
                    WeatherStatus.RAINY,
                    WeatherStatus.RAINY,
                    WeatherStatus.SNOWY,
                    WeatherStatus.RAINY,
                    WeatherStatus.SUNNY,
                    WeatherStatus.SUNNY,
                    WeatherStatus.SNOWY,
                    WeatherStatus.CLOUDY,
                ),
                HeadsUpMessage.SNOWY,
            ),
            (
                (
                    WeatherStatus.RAINY,
                    WeatherStatus.RAINY,
                    WeatherStatus.SNOWY,
                    WeatherStatus.RAINY,
                    WeatherStatus.SUNNY,
                    WeatherStatus.SUNNY,
                    WeatherStatus.RAINY,
                    WeatherStatus.CLOUDY,
                ),
                HeadsUpMessage.HEAVY_RAIN,
            ),
            (
                (
                    WeatherStatus.CLOUDY,
                    WeatherStatus.RAINY,
                    WeatherStatus.SNOWY,
                    WeatherStatus.CLOUDY,
                    WeatherStatus.SUNNY,
                    WeatherStatus.SUNNY,
                    WeatherStatus.RAINY,
                    WeatherStatus.CLOUDY,
                ),
                HeadsUpMessage.RAIN,
            ),
            (
                (
                    WeatherStatus.CLOUDY,
                    WeatherStatus.RAINY,
                    WeatherStatus.SNOWY,
                    WeatherStatus.CLOUDY,
                    WeatherStatus.SUNNY,
                    WeatherStatus.SUNNY,
                    WeatherStatus.CLOUDY,
                    WeatherStatus.CLOUDY,
                ),
                HeadsUpMessage.OTHERS,
            ),
        ],
    )
    def test_generate_message(
        self, weather_statuses: Tuple[WeatherStatus], expected_message: str, get_forecast: Callable[..., Forecast]
    ):
        forecasts = (
            get_forecast(hour_offset=i * 6, status=status) for i, status in enumerate(weather_statuses, start=1)
        )

        message = DefaultHeadsUpMessageStrategy.generate_message(tuple(forecasts))

        assert message == expected_message
