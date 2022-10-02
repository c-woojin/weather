FROM python:3.10-slim

ARG REQUIREMENT="requirements.txt"

COPY $REQUIREMENT /tmp/
RUN pip install -r /tmp/$REQUIREMENT

RUN mkdir -p /src
COPY src/ /src/
RUN pip install -e /src
COPY tests/ /tests/

WORKDIR /src
CMD ["uvicorn", "weather.entrypoint.main:app", "--host", "0.0.0.0", "--port", "8000"]
