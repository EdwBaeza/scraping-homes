FROM python:3.9-alpine

WORKDIR /app
RUN python -m pip install --upgrade pip

COPY ./requirements/local.txt .
RUN pip install -r local.txt

COPY models/ models/
COPY spiders/ spiders/
COPY validators/ validators/
COPY tests/ tests/
COPY .env .
COPY run.py .
