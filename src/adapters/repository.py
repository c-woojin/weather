import abc
import asyncio
from datetime import datetime
from typing import Dict, Type, Tuple

import aiohttp
from aiohttp import ClientSession

from src.adapters.errors import InvalidMessageStrategy
from src.configs import DROOM_WEATHER_API_BASE_URL, DROOM_API_KEY
from src.domain.message_strategies import (
    AbstractGreetingMessageStrategy,
    DefaultGreetingMessageStrategy,
    AbstractTemperatureMessageStrategy,
    DefaultTemperatureMessageStrategy,
    AbstractHeadsUpMessageStrategy,
    DefaultHeadsUpMessageStrategy,
)
from src.domain.models import WeatherSummary, Location, Weather, Forecast

MESSAGE_STRATEGY: Dict[
    str,
    Tuple[
        Type[AbstractGreetingMessageStrategy],
        Type[AbstractTemperatureMessageStrategy],
        Type[AbstractHeadsUpMessageStrategy],
    ],
] = dict(default=(DefaultGreetingMessageStrategy, DefaultTemperatureMessageStrategy, DefaultHeadsUpMessageStrategy))


class AbstractWeatherSummaryRepository(abc.ABC):
    @abc.abstractmethod
    def get_weather_summary(self, location: Location, message_strategy: str) -> WeatherSummary:
        raise NotImplementedError


class DroomWeatherSummaryRepository(AbstractWeatherSummaryRepository):
    def __init__(self):
        self.base_url: str = DROOM_WEATHER_API_BASE_URL
        self.endpoints: Dict[str, str] = dict(
            current="/current",
            historical="/historical/hourly",
            forecast="/forecast/hourly",
        )
        self.api_key = DROOM_API_KEY

    async def get_weather_summary(self, location: Location, message_strategy: str) -> WeatherSummary:
        try:
            greeting_strategy, temperature_strategy, heads_up_strategy = MESSAGE_STRATEGY[message_strategy]
        except KeyError:
            raise InvalidMessageStrategy(f"Invalid message strategy({message_strategy})")

        async with aiohttp.ClientSession(self.base_url) as session:
            aws = [
                self._get_weathers(location=location, session=session),
                self._get_forecasts(location=location, session=session),
            ]
            weathers, forecasts = await asyncio.gather(*aws)

        return WeatherSummary(
            location=location,
            date_time=datetime.now(),
            weathers=weathers,
            forecasts=forecasts,
            greeting_message_strategy=greeting_strategy,
            temperature_message_strategy=temperature_strategy,
            heads_up_message_strategy=heads_up_strategy,
        )

    async def _get_weathers(self, location: Location, session: ClientSession) -> Tuple[Weather]:
        aws = [
            self._get_weather(location=location, hour_offset=hour_offset * -6, session=session)
            for hour_offset in range(5)
        ]
        weathers = await asyncio.gather(*aws)
        weathers = (w for w in weathers if isinstance(w, Weather))
        return tuple(weathers)

    async def _get_forecasts(self, location: Location, session: ClientSession) -> Tuple[Forecast]:
        aws = [
            self._get_forecast(location=location, hour_offset=hour_offset * 6, session=session)
            for hour_offset in range(1, 9)
        ]
        forecasts = await asyncio.gather(*aws)
        forecasts = (f for f in forecasts if isinstance(f, Forecast))
        return tuple(forecasts)

    async def _get_weather(self, location: Location, hour_offset: int, session: ClientSession) -> Weather:
        endpoint = self.endpoints["current"]
        params = dict(lat=location.latitude, lon=location.longitude, api_key=self.api_key)
        if hour_offset != 0:
            endpoint = self.endpoints["historical"]
            params["hour_offset"] = hour_offset

        async with session.get(endpoint, params=params) as resp:
            result = await resp.json()

        return Weather(
            hour_offset=hour_offset,
            status=result["code"],
            temperature=result["temp"],
            precipitation=result["rain1h"],
        )

    async def _get_forecast(self, location: Location, hour_offset: int, session: ClientSession) -> Forecast:
        endpoint = self.endpoints["forecast"]
        params = dict(lat=location.latitude, lon=location.longitude, hour_offset=hour_offset, api_key=self.api_key)

        async with session.get(endpoint, params=params) as resp:
            result = await resp.json()

        return Forecast(hour_offset=hour_offset, status=result["code"])
