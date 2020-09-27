#PYTHON VERSION
FROM python:3.8.3-alpine

#SET PYTHON ENV
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

###postgress dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

#MAINTAINE

#initialize the app
RUN mkdir /tweet
WORKDIR /tweet
COPY requirements.txt /tweet/
#install dependencies

RUN pip install -r requirements.txt
COPY . /tweet/
