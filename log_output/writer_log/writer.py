import uuid
import logging
from datetime import datetime, timezone
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


def main():
    """Main function to run the logging loop."""
    # Generate random string on startup
    random_string = str(uuid.uuid4())
    logger = setup_logger()
    LOG_FILE = '/usr/src/app/files/data.log'
    
    logger.info(f"Starting log writer with random string: {random_string}")
    
    try:
        while True:
            # Update timestamp
            now = datetime.now(timezone.utc)
            current_timestamp = now.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
            
            # Log the output
            line = f"{current_timestamp}: {random_string}\n"
            logger.info(line.strip())
            
            with open(LOG_FILE, 'a') as f:
                f.write(line)
            
            # Wait 5 seconds
            time.sleep(5)
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received. Shutting down gracefully.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        logger.info("Log writer stopped.")


if __name__ == "__main__":
    main()