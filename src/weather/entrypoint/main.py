from fastapi import FastAPI, HTTPException, Query
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from weather.adapters import repository
from weather.adapters.errors import WeatherSummaryRepositoryTimeout
from weather.services import services

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(status_code=400, content=str(exc))


@app.get("/summary")
async def summary(lat: float = Query(ge=-90, le=90), lon: float = Query(ge=-180, le=180)):
    repo = repository.DroomWeatherSummaryRepository()

    try:
        summary_messages = await services.get_weather_summary_messages(latitude=lat, longitude=lon, repo=repo)
    except WeatherSummaryRepositoryTimeout:
        raise HTTPException(status_code=408)
    except Exception:
        raise HTTPException(status_code=500)

    return dict(summary=summary_messages)
