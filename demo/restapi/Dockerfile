# Dockerfile
FROM python:3.9-slim

LABEL maintainer="Christopher Le"

WORKDIR /app

ENV PORT=5001

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE $PORT

CMD ["python", "app.py"]
