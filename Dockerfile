FROM python:3.11-slim

ENV PYTHONDONTWRITEBYECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./backend /code