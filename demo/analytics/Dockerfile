FROM python:3.9-slim

LABEL maintainer="Christopher Le"

# Set working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install requirements
RUN pip install -r requirements.txt

# Copy the remaining files
COPY . .

# Expose the desired port
ENV PORT=5001
EXPOSE $PORT

# Set the command to run the application
CMD ["python", "app.py"]
