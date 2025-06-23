# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# ---- START OF FIX ----
# Install system dependencies needed to build mysqlclient
RUN apt-get update && apt-get install -y \
    pkg-config \
    default-libmysqlclient-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*
# ---- END OF FIX ----

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# Also upgrading pip as suggested by the log
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend source code into the container
COPY ./src /app/src

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
# We use --host 0.0.0.0 to make it accessible from outside the container
CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]