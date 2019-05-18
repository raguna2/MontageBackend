FROM python:3.7.2-slim-stretch

EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /app/
ENV MONTAGE_GUNICORN_WORKERS=4

RUN mkdir -p /app
COPY . /app/
WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends && \
    apt-get install -y default-libmysqlclient-dev && \
    apt-get install -y gcc && \
    pip install -r dev-requires.txt

CMD gunicorn -w $MONTAGE_GUNICORN_WORKERS\
    --log-level INFO\
    -b 0.0.0.0:$PORT\
    -e DJANGO_SETTINGS_MODULE=settings.common\
    lbc_match.wsgi:application
