FROM python:3.11-slim

WORKDIR /app

# Copy dependencies file (if needed later)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
# Copy the Python application

COPY pong.py .

# Run the application
CMD ["python", "pong.py"]
