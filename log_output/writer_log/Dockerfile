FROM python:3.11-slim

WORKDIR /usr/src/app

# Copy the Python application
COPY writer.py .

# Environment variable for Flask
ENV PORT=3000

# Run the application
CMD ["python", "writer.py"]
