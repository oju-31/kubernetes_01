# Use official Python runtime as base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install PostgreSQL client 18 from the official PGDG repo
RUN apt-get update \
    && apt-get install -y postgresql-client
    # && rm -rf /var/lib/apt/lists/*
   
# Copy dependencies file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app
COPY backup.py .

# Run the app
CMD ["python", "backup.py"]
