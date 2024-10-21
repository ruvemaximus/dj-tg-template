FROM python:3.12-slim

COPY . /app/
WORKDIR /app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt update && apt install -y supervisor && \
    apt clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --upgrade pip && \
    pip install --no-cache-dir django python-telegram-bot pillow python-dotenv && \
    mkdir -p /var/log/supervisor && \
    /app/manage.py migrate

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
CMD ["/usr/bin/supervisord"]