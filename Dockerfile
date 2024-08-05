# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN python -m venv .venv && \
    . .venv/bin/activate && \
    pip install --no-cache-dir -r requirements.txt

# Create the necessary directories and initialize the database
RUN . .venv/bin/activate && flask db upgrade

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "wsgi:app"]