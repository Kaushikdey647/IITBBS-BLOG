# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP wsgi.py
ENV FLASK_RUN_HOST 0.0.0.0

# Set the working directory
WORKDIR /app

# Create and activate virtual environment, then install dependencies
RUN python -m venv .venv && \
    source .venv/bin/activate && \
    pip install --no-cache-dir -r requirements.txt

# Copy the entire application to the container
COPY . /app/

# Create the necessary directories and initialize the database
RUN flask db upgrade

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "wsgi:app"]