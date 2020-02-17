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
ENV LANG=${LOCALE}
ENV TZ=${TZ}

WORKDIR ${APPDIR}/montage/

EXPOSE 8000
CMD [ \
  "gunicorn", \
  "-w",                     "2", \
  "-b",                     "127.0.0.1:8000", \
  "--max-requests",         "47", \
  "--max-requests-jitter",  "5", \
  "--timeout",              "3600", \
  "--access-logfile",       "-", \
  "--error-logfile",        "-", \
  "--capture-output", \
  "montage.wsgi" \
]
