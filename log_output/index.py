import uuid
import os
import logging
from datetime import datetime, timezone
from flask import Flask, jsonify
import threading
import time


def setup_logger():
    """Set up and configure the logger."""
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    # Create console handler
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    # Add handler to logger
    if not logger.handlers:
        logger.addHandler(handler)

    return logger


# Global variables to store the current state
current_timestamp = None
random_string = str(uuid.uuid4())  # Generate on startup
logger = setup_logger()

app = Flask(__name__)


def update_timestamp():
    """Background thread to update timestamp every 5 seconds and log."""
    global current_timestamp
    while True:
        # Update timestamp
        now = datetime.now(timezone.utc)
        current_timestamp = now.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        
        # Log the output
        logger.info(f"{current_timestamp}: {random_string}")
        
        # Wait 5 seconds
        time.sleep(5)


@app.route("/")
def home():
    """Home endpoint with basic info."""
    return "Log Output Application - visit /status for current status"


@app.route("/status")
def status():
    """Endpoint to get current timestamp and random string."""
    return f"{current_timestamp}: {random_string}"


if __name__ == "__main__":
    # Start background thread for logging
    log_thread = threading.Thread(target=update_timestamp, daemon=True)
    log_thread.start()
    
    # Get port from environment, default to 3000
    port = int(os.getenv("PORT", 3000))
    
    # Log the server start message
    logger.info(f"Server started on port {port}")
    # logger.info(f"Generated random string: {random_string}")
    
    # Run Flask
    app.run(host="0.0.0.0", port=port)