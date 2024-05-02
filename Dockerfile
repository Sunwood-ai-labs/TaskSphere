FROM python:3.11-slim

WORKDIR /app

RUN apt update
RUN apt install -y curl

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
