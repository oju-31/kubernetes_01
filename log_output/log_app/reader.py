from flask import Flask
import os
import logging
import uuid
from datetime import datetime, timezone
import requests

app = Flask(__name__)


def setup_logger():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    return logger


def get_ping_pong_count():
    """Fetch the ping/pong count from pong.com"""
    try:
        response = requests.get('http://pong-svc:2345/pings', timeout=5)
        response.raise_for_status()
        # Parse JSON response and extract pings count
        data = response.json()
        count = data.get('pings', 0)
        return count
    except (requests.RequestException, ValueError) as e:
        logger = setup_logger()
        logger.error(f"Failed to fetch ping/pong count: {e}")
        return 0  # Default to 0 if request fails


@app.route('/')
def read_file():
    # Generate random string on startup
    random_string = str(uuid.uuid4())
    logger = setup_logger()
    
    # Update timestamp
    now = datetime.now(timezone.utc)
    current_timestamp = now.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    line = f"{current_timestamp}: {random_string}.\n"
    
    # Get ping/pong count
    ping_pong_count = get_ping_pong_count()
    
    # Format the response
    response_text = f"{line}Ping / Pongs: {ping_pong_count}"
    
    # Log the output
    logger.info(response_text)
    
    # Return the formatted response
    return response_text, 200, {'Content-Type': 'text/plain'}


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port)
