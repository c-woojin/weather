from fastapi import FastAPI

from src.adapters import repository
from src.domain import models
from src.services import services

app = FastAPI()


@app.get("/summary")
async def summary(lat: float, lon: float):
    repo = repository.DroomWeatherSummaryRepository()
    location = models.Location(latitude=lat, longitude=lon)
    summary_messages = await services.get_weather_summary_messages(location=location, repo=repo)
    return dict(summary=summary_messages)
