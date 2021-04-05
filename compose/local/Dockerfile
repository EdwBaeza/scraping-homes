FROM python:3.8-alpine

WORKDIR /app
RUN python -m pip install --upgrade pip
RUN apk update\
  && apk add --virtual build-deps build-base libffi-dev gcc python3-dev musl-dev\
  && apk add libffi-dev py-cffi \
  && apk add postgresql-dev\
  && apk add --update curl\
  && rm -rf /var/cache/apk/*\
  && apk add wget

RUN apk add chromium chromium-chromedriver

# install dependencies is here to be trapped by docker cache layer
COPY ./requirements/base.txt .
COPY ./requirements/local.txt .
RUN pip install -r local.txt

COPY commands/ commands/
COPY libs/ libs/
COPY models/ models/
COPY repository/ repository/
COPY spiders/ spiders/
COPY tests/ tests/
COPY validators/ validators/
COPY .env .
COPY main.py .
