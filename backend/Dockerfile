FROM python:3.11-slim

# set environments vars
ENV PYTHONDONTWRITEBYECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install os dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*
    
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY entrypoint.sh  /entrypoint.sh

EXPOSE 8000

# Gunicorn server

RUN chmod +x /entrypoint.sh
CMD [ "/entrypoint.sh" ]