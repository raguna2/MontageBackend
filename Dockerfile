# vim: ft=dockerfile ts=2 sw=2 et
FROM python:3.7-slim-stretch

# Install tox in an image (1: install, 0: not)
ARG WITHTOX="0"
# Keep wheelhouse in an image (1: keep, 0: not)
ARG KEEPWHEELHOUSE="1"

ARG RUNTIME_DEPS="locales"
ARG CHARSET="UTF-8"
ARG LOCALE="ja_JP.UTF-8"
ARG TZ="Asia/Tokyo"
ARG APPDIR="/var/www/montage"

RUN mkdir -p ${APPDIR}

# Copy files are requires to install dependencies
COPY requirements.txt ${APPDIR}/requirements.txt


WORKDIR ${APPDIR}
RUN apt-get update && \
    apt-get install -y --no-install-recommends && \
    apt-get install -y default-libmysqlclient-dev && \
    apt-get install -y gcc && \
    pip install -r requirements.txt

# Copy all files
COPY . ${APPDIR}

# For testing
RUN \
  # Install tox for testing
  if [ "${WITHTOX}" = "1" ] ; then \
    pip install --no-cache-dir virtualenv==16.7.9 tox && \
    mkdir -p ${APPDIR}/.tox ${APPDIR}/.pytest_cache; \
fi
# This volume is necessary for preserving permissions
VOLUME ${APPDIR}/.tox

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=${APPDIR}/montage
ENV PYTHONUNBUFFERED 1

ENV LANG=${LOCALE}
ENV TZ=${TZ}

# heroku上では環境変数でPORTを設定しないと疎通できない.EXPOSEは設定しても意味がない.
ENV PORT=8000
ENV MONTAGE_GUNICORN_WORKERS=2

WORKDIR ${APPDIR}/montage/

EXPOSE 8000
CMD gunicorn -w $MONTAGE_GUNICORN_WORKERS\
    --log-level INFO\
    -b 0.0.0.0:$PORT\
    -e DJANGO_SETTINGS_MODULE=montage.settings\
    montage.wsgi:application
