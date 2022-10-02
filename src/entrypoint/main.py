from fastapi import FastAPI, HTTPException, Query
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.adapters import repository
from src.adapters.errors import APITimeout
from src.domain import models
from src.services import services

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(status_code=400, content=str(exc))


@app.get("/summary")
async def summary(lat: float = Query(ge=-90, le=90), lon: float = Query(ge=-180, le=180)):
    try:
        repo = repository.DroomWeatherSummaryRepository()
        location = models.Location(latitude=lat, longitude=lon)
        summary_messages = await services.get_weather_summary_messages(location=location, repo=repo)
    except APITimeout:
        raise HTTPException(status_code=408)
    except Exception:
        raise HTTPException(status_code=500)
    return dict(summary=summary_messages)
