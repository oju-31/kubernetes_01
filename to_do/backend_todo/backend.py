from flask import Flask, jsonify, request
from flask_cors import CORS
from os import getenv
import psycopg2
import psycopg2.extras
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
PORT = int(getenv('PORT'))

# Database connection from environment variables
def get_db():
    return psycopg2.connect(
        host=getenv('DATABASE_HOST'),
        port=getenv('DATABASE_PORT', '5432'),
        user=getenv('DATABASE_USER'),
        password=getenv('DATABASE_PASSWORD'),
        database=getenv('DATABASE_NAME')
    )

# Initialize database table
def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    # Create todos table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id SERIAL PRIMARY KEY,
            text TEXT NOT NULL
        )
    ''')
    
    # Insert default todos if table is empty
    cursor.execute('SELECT COUNT(*) FROM todos')
    if cursor.fetchone()[0] == 0:
        default_todos = [
            ("Learn JavaScript",),
            ("Learn React",),
            ("Build a project",)
        ]
        cursor.executemany('INSERT INTO todos (text) VALUES (%s)', default_todos)
    
    conn.commit()
    cursor.close()
    conn.close()


@app.route('/')
def root():
    return "OK", 200


@app.route('/todos', methods=['GET'])
def get_todos():
    """Get all todos"""
    logger.info(f"GET /todos - IP: {request.remote_addr}")
    
    conn = get_db()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    cursor.execute('SELECT id, text FROM todos ORDER BY id')
    todos = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    logger.info(f"GET /todos - Returned {len(todos)} todos")
    return jsonify(list(todos))


@app.route('/todos', methods=['POST'])
def create_todo():
    """Create a new todo"""
    client_ip = request.remote_addr
    data = request.get_json()
    
    # Log incoming request
    logger.info(f"POST /todos - IP: {client_ip} - Data: {data}")
    
    if not data or 'text' not in data:
        logger.warning(f"POST /todos - IP: {client_ip} - ERROR: Missing todo text")
        return jsonify({"error": "Todo text is required"}), 400
    
    todo_text = data['text']
    
    # Check length and log if too long
    if len(todo_text) > 140:
        logger.warning(f"POST /todos - IP: {client_ip} - BLOCKED: Todo too long ({len(todo_text)} chars) - '{todo_text[:50]}...'")
        return jsonify({"error": "Todo must be 140 characters or less"}), 400
    
    conn = get_db()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    cursor.execute(
        'INSERT INTO todos (text) VALUES (%s) RETURNING id, text',
        (todo_text,)
    )
    
    new_todo = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    
    logger.info(f"POST /todos - IP: {client_ip} - SUCCESS: Created todo #{new_todo['id']} - '{todo_text}'")
    return jsonify(dict(new_todo)), 201

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=PORT, debug=True)
