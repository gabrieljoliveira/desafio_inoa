FROM python:3

RUN python -m pip install -U pip

COPY ./requirements.txt /requirements.txt

RUN	pip install -r /requirements.txt 

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser user
USER user
