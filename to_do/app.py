import os
import logging
from flask import Flask

# Set up logging
def setup_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    # Create console handler
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    # Add handler to logger
    if not logger.handlers:
        logger.addHandler(handler)

    return logger

app = Flask("todo-app")

@app.route("/")
def home():
    return "Hello from the Todo App!"


logger = setup_logger()
# Get port from environment, default to 5000
port = int(os.getenv("PORT", 3000))

# Log the server start message
logger.info(f"Server started in port {port}")

# Run Flask
app.run(host="0.0.0.0", port=port)
