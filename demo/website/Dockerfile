# Dockerfile
FROM python:3.9-slim

LABEL maintainer="Christopher Le"
LABEL version="1.0"

WORKDIR /app

ENV PORT=5001
ENV AUTHOR="Christopher Le"

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app.py .
COPY templates ./templates

EXPOSE $PORT

CMD ["python3", "app.py"]

