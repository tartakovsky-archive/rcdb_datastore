FROM python:3.7-slim-buster
ENV PYTHONUNBUFFERED 1
RUN pip install -U --no-cache-dir pip
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt
WORKDIR /app
COPY ./ /app/
