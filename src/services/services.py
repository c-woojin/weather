from typing import Dict

from src.adapters.repository import AbstractWeatherSummaryRepository
from src.domain.models import Location


async def get_weather_summary_messages(location: Location, repo: AbstractWeatherSummaryRepository) -> Dict[str, str]:
    weather_summary = await repo.get_weather_summary(location=location, message_strategy="default")
    summary_messages = dict(
        greeting=weather_summary.generate_greeting_message(),
        temperature=weather_summary.generate_temperature_message(),
        heads_up=weather_summary.generate_heads_up_message(),
    )
    return summary_messages
