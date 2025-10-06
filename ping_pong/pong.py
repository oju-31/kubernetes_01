from flask import Flask, jsonify
from os import getenv
import psycopg2
import time
import logging

app = Flask(__name__)

# Database connection parameters from environment variables
PORT = int(getenv('PORT'))
DATABASE_CONFIG = {
    'host': getenv('DATABASE_HOST'),
    'port': int(getenv('DATABASE_PORT', '5432')),
    'user': getenv('DATABASE_USER', 'postgres'),
    'password': getenv('DATABASE_PASSWORD', 'password'),
    'database': getenv('DATABASE_NAME', 'pongdb')
}


def setup_logger():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    return logger


logger = setup_logger()


def get_db_connection():
    """Create and return a database connection"""
    try:
        conn = psycopg2.connect(**DATABASE_CONFIG)
        return conn
    except psycopg2.Error as e:
        logger.error(f"Database connection error: {e}")
        return None


def init_database():
    """Initialize the database table if it doesn't exist"""
    max_retries = 5
    retry_count = 0

    while retry_count < max_retries:
        try:
            conn = get_db_connection()
            if conn:
                cursor = conn.cursor()

                # Create table if it doesn't exist
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS ping_counter (
                        id SERIAL PRIMARY KEY,
                        counter INTEGER NOT NULL,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)

                # Check if we have any records, if not, insert initial counter
                cursor.execute("SELECT COUNT(*) FROM ping_counter")
                count = cursor.fetchone()[0]

                if count == 0:
                    cursor.execute(
                        "INSERT INTO ping_counter (counter) VALUES (0)"
                    )
                    logger.info("Initialized ping counter in database")

                conn.commit()
                cursor.close()
                conn.close()
                logger.info("Database initialized successfully")
                return True

        except psycopg2.Error as e:
            retry_count += 1
            logger.error(f"Database init attempt {retry_count} failed: {e}")
            if retry_count < max_retries:
                logger.info(f"Retrying in 2 seconds...")
                time.sleep(2)

    logger.error("Failed to initialize database after maximum retries")
    return False


def get_current_counter():
    """Get the current counter value from database"""
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT counter FROM ping_counter ORDER BY id DESC LIMIT 1"
            )
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            return result[0] if result else 0
    except psycopg2.Error as e:
        logger.error(f"Error getting counter: {e}")
        return 0


def increment_counter():
    """Increment the counter in database and return new value"""
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()

            # Get current counter and increment
            cursor.execute(
                "SELECT counter FROM ping_counter ORDER BY id DESC LIMIT 1"
            )
            result = cursor.fetchone()
            current_counter = result[0] if result else 0
            new_counter = current_counter + 1

            # Insert new counter value
            cursor.execute(
                "INSERT INTO ping_counter (counter) VALUES (%s)",
                (new_counter,)
            )

            conn.commit()
            cursor.close()
            conn.close()
            return new_counter
    except psycopg2.Error as e:
        logger.error(f"Error incrementing counter: {e}")
        return 0


@app.route('/')
def root():
    return "OK", 200


@app.route('/pingpong', methods=['GET'])
def pingpong():
    # Get current counter value before incrementing
    current_counter = get_current_counter()
    response = f"pong {current_counter}"

    # Increment counter in database
    increment_counter()

    return response


@app.route('/pings', methods=['GET'])
def get_pings():
    """Return the current ping count as JSON"""
    counter = get_current_counter()
    return jsonify({"pings": counter})


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    try:
        conn = get_db_connection()
        if conn:
            conn.close()
            return jsonify({"status": "healthy", "database": "connected"})
        else:
            return jsonify(
                {"status": "unhealthy", "database": "disconnected"}
                ), 500
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500


if __name__ == '__main__':
    logger.info("Starting Ping-Pong application...")
    logger.info(
        f"Database config: {DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}"
    )

    # Initialize database on startup
    if init_database():
        logger.info("Database ready, starting Flask app...")
        app.run(debug=True, host='0.0.0.0', port=PORT)
    else:
        logger.error("Failed to initialize database, exiting...")
        exit(1)
