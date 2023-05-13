FROM python:3.8-slim

# Install system dependencies
RUN apt-get update && apt-get install -y gcc ffmpeg

# Set working directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Set the environment variable for PyDub to use ffmpeg
ENV PATH="/usr/bin/ffmpeg:${PATH}"

# Start the application
CMD gunicorn main:app --bind 0.0.0.0:$PORT
