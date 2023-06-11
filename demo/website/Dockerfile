# Dockerfile
FROM python:3.9-slim

WORKDIR /app

ENV PORT=5001

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app.py .

EXPOSE $PORT

CMD ["python3", "app.py"]

