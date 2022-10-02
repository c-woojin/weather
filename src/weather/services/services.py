from typing import Dict

from weather.adapters.repository import AbstractWeatherSummaryRepository
from weather.domain.models import Location


async def get_weather_summary_messages(
    latitude: float, longitude: float, repo: AbstractWeatherSummaryRepository
) -> Dict[str, str]:
    location = Location(latitude=latitude, longitude=longitude)
    weather_summary = await repo.get_weather_summary(location=location, message_strategy="default")
    summary_messages = dict(
        greeting=weather_summary.generate_greeting_message(),
        temperature=weather_summary.generate_temperature_message(),
        heads_up=weather_summary.generate_heads_up_message(),
    )
    return summary_messages
