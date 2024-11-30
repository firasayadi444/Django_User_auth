# Use the official Python image as the base image
FROM python:3.12-slim

# Install dependencies for mysqlclient, Selenium, and build tools
RUN apt-get update && apt-get install -y \
    pkg-config \
    libmariadb-dev \
    build-essential \
    chromium \
    chromium-driver \
    wget \
    curl \
    unzip \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory (your project) to /app inside the container
COPY . /app/

# Set the DJANGO_SETTINGS_MODULE to the correct settings file
ENV DJANGO_SETTINGS_MODULE=auth.settings

# Install virtualenv and create an isolated environment
RUN pip install --no-cache-dir virtualenv && virtualenv /venv

# Activate the virtual environment and install dependencies
RUN /venv/bin/pip install --no-cache-dir -r requirements.txt pytest pytest-django selenium

# Use the virtual environment in the container
ENV PATH="/venv/bin:$PATH"

# Set environment variables for Selenium
ENV DISPLAY=:99

# Expose port 8000 to access the app
EXPOSE 8000

# Default command to run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
