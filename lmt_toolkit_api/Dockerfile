FROM python:alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apk update && apk add --no-cache \
    build-base \
    gcc \
    musl-dev \
    gfortran \
    python3-dev \
    linux-headers \
    sqlite \
    tk \
    netcat-openbsd \
    libffi-dev \
    pkgconfig \
    cmake \
    openblas-dev \
    lapack-dev \
    bash

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install -e .

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
RUN dos2unix /entrypoint.sh

ENTRYPOINT [ "bash", "/entrypoint.sh" ]