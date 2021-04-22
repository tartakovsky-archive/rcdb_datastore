FROM python:3.7-slim-buster
ENV PYTHONUNBUFFERED 1
RUN pip install -U --no-cache-dir pip
COPY requirements.txt /app/
COPY rcdb_commons/requirements.txt /app/requirements.rcdb_commons.txt
RUN pip install --no-cache-dir -r /app/requirements.txt -r requirements.rcdb_commons.txt
WORKDIR /app
COPY ./ /app/
