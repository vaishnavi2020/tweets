FROM python:3.9-slim

RUN pip install kafka-python

WORKDIR /app

COPY producer.py /app/producer.py
COPY sentiment_10000.csv /app/sentiment_10000.csv

CMD ["python", "/app/producer.py"]