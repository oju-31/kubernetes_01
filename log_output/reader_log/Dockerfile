FROM python:3.11-slim

WORKDIR /usr/src/app

# Copy dependencies file (if needed later)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
# Copy the Python application

COPY reader.py .

# Environment variable for Flask
ENV PORT=3000

# Run the application
CMD ["python", "reader.py"]
