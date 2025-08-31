import uuid
import time
import logging
from datetime import datetime, timezone


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


def main():
    logger = setup_logger()
    # Generate random string on startup
    random_string = str(uuid.uuid4())

    try:
        while True:
            # Output the string with timestamp
            now = datetime.now(timezone.utc)
            timestamp = now.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
            logger.info(f"{timestamp}: {random_string}")
            # Wait 5 seconds
            time.sleep(5)
    except KeyboardInterrupt:
        logger.info("Timer stopped.")


if __name__ == "__main__":
    main()
