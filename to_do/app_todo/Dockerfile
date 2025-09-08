# Use official Python runtime as base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy dependencies file (if needed later)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app
COPY app.py .
COPY templates/ ./templates/

# Environment variable for Flask
ENV PORT=3000

# Run the app
CMD ["python", "app.py"]
