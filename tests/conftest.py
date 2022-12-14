from typing import Optional

import pytest
from faker import Faker

from weather.domain.constants import WeatherStatus
from weather.domain.models import Weather, Forecast

fake = Faker()


@pytest.fixture(scope="function")
def get_weather():
    def _weather(
        hour_offset: Optional[int] = None,
        status: Optional[WeatherStatus] = None,
        temperature: Optional[float] = None,
        precipitation: Optional[float] = None,
    ):
        return Weather(
            hour_offset=fake.random_choices(elements=(0, -6, -12, -18, -24)) if hour_offset is None else hour_offset,
            status=fake.random_choices(elements=WeatherStatus) if status is None else status,
            temperature=fake.pyfloat(min_value=-100.0, max_value=100.0, right_digits=2)
            if temperature is None
            else temperature,
            precipitation=fake.pyfloat(positive=True, max_value=1000.0, right_digits=2)
            if precipitation is None
            else precipitation,
        )

    return _weather


@pytest.fixture(scope="function")
def get_forecast():
    def _forecast(
        hour_offset: Optional[int] = None,
        status: Optional[WeatherStatus] = None,
    ):
        return Forecast(
            hour_offset=fake.random_choices(elements=(6, 12, 18, 24, 30, 36, 42, 48))
            if hour_offset is None
            else hour_offset,
            status=fake.random_choices(elements=WeatherStatus) if status is None else status,
        )

    return _forecast
