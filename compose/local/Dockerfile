FROM python:3.8-alpine

WORKDIR /app
RUN python -m pip install --upgrade pip
RUN apk update \
  # psycopg2 dependencies
  && apk add --virtual build-deps build-base libffi-dev gcc python3-dev musl-dev \
  && apk add postgresql-dev

COPY ./requirements/base.txt .
COPY ./requirements/local.txt .
RUN pip install -r local.txt

COPY models/ models/
COPY spiders/ spiders/
COPY validators/ validators/
COPY tests/ tests/s
COPY .env .
COPY run.py .
