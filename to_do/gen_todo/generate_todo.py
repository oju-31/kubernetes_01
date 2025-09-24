import requests
import json
from datetime import datetime
from os import getenv
import logging


BACKEND_API_URL = f'{getenv('TODO_API_BASE_URL')}/todos'
WIKIPEDIA_RANDOM_URL = "https://en.wikipedia.org/wiki/Special:Random"


def setup_logger():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    return logger

logger = setup_logger()


def get_random_wikipedia_article():
    """Get a random Wikipedia article URL by following the redirect"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (compatible; TodoBot/1.0)'}
        response = requests.get(
            WIKIPEDIA_RANDOM_URL, 
            headers=headers, 
            allow_redirects=False
        )
        if response.status_code in [301, 302]:
            # Extract the actual article URL from Location header
            article_url = response.headers.get('Location')
            if article_url:
                return article_url
            else:
                logger.info("No Location header found in response")
                return None
        else:
            logger.error(f"Unexpected status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        logger.error(f"Error fetching random Wikipedia article: {e}")
        return None


def create_todo_item(text):
    """Send a POST request to create a new todo item"""
    try:
        headers = {'Content-Type': 'application/json'}
        data = {'text': text}
        response = requests.post(
            BACKEND_API_URL, 
            headers=headers, 
            data=json.dumps(data)
        )
        if response.status_code == 201:
            todo = response.json()
            print(f"✅ Todo created successfully: {todo}")
            return True
        else:
            print(f"❌ Failed to create todo. Status: {response.status_code}, Response: {response.text}")
            return False
    except requests.RequestException as e:
        print(f"❌ Error creating todo: {e}")
        return False


def main():
    """Generate a new todo with a random Wikipedia article"""
    logger.info(f"🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Generating Wikipedia todo...")
    # Get random Wikipedia article URL
    article_url = get_random_wikipedia_article()
    
    if article_url:
        todo_text = f"Read {article_url}"
        success = create_todo_item(todo_text)
        if success:
            logger.info(f"📖 New reading todo added: {article_url}")
            return 0  # Success exit code
        else:
            logger.error("Failed to create todo item")
            return 1  # Error exit code
    else:
        logger.error("❌ Failed to get random Wikipedia article")
        return 1  # Error exit code

if __name__ == "__main__":
    exit(main())
