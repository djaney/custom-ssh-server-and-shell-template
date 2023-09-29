FROM python:3.10.0-alpine
WORKDIR /app
RUN apk update && \
    apk add py3-pip build-base && \
    python3 -m pip install --upgrade pip
RUN mkdir -p /app
COPY main.py /app
COPY requirements.txt /app
COPY src /app/src
RUN python3 -m pip install -r /app/requirements.txt
