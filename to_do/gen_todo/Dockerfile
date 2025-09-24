# Use official Python runtime as base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy dependencies file (if needed later)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app
COPY generate_todo.py .

# Run the app
CMD ["python", "generate_todo.py"]
