FROM python:alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apk update && apk add --no-cache \
    gcc \
    musl-dev \
    python3-dev \
    linux-headers \
    sqlite \
    tk \
#    libffi-dev \
#    build-base \
#    pkgconfig \
    bash

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install -e .

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
RUN dos2unix /entrypoint.sh

ENTRYPOINT [ "bash", "/entrypoint.sh" ]