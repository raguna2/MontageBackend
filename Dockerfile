FROM python:3.7.2-slim-stretch

ARG PYTHONDEVREQUIRES="0"

EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED 1
ENV MONTAGE_GUNICORN_WORKERS=4

RUN mkdir -p /app
COPY . /app/
WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends && \
    apt-get install -y default-libmysqlclient-dev && \
    apt-get install -y gcc && \
    pip install -r requirements.txt

RUN \
    # Install dev-requires for testing
    if [ "${PYTHONDEVREQUIRES}" = "1" ] ; then \
        pip install -r dev-requires.txt; \
    fi

CMD gunicorn -w $MONTAGE_GUNICORN_WORKERS\
    --log-level INFO\
    -b 0.0.0.0:$PORT\
    -e DJANGO_SETTINGS_MODULE=montage.settings.prod\
    montage.wsgi:application
