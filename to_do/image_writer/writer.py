from os import getenv
import time
import logging
import urllib.request
import signal
import sys
from datetime import datetime, timezone
from pathlib import Path


img_url = getenv('IMG_URL')
# IMG_FOLDER = '/usr/src/app/files'
IMG_FOLDER = getenv('IMG_FOLDER')


def setup_logger():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    return logger


def download_image(url, filepath, logger):
    try:
        urllib.request.urlretrieve(url, filepath)
        logger.info(f"Downloaded image to {filepath}")
        return True
    except Exception as e:
        logger.error(f"Download failed: {e}")
        return False


def cleanup_old_images(files_dir, current_file):
    for file_path in Path(files_dir).glob("image_*.jpg"):
        if file_path != current_file:
            file_path.unlink()


def main():
    """Main function to run the logging loop."""
    logger = setup_logger()
    files_dir = Path(IMG_FOLDER)
    files_dir.mkdir(exist_ok=True)

    try:
        while True:
            # Update timestamp
            now = datetime.now(timezone.utc)
            timestamp = now.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
            image_path = files_dir / f"image_{timestamp}.jpg"
            
            if download_image(img_url, image_path, logger):
                cleanup_old_images(files_dir, image_path)
            
            time.sleep(600)  # 10 minutes
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received. Shutting down gracefully.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        logger.info("Log writer stopped.")


if __name__ == "__main__":
    main()