from flask import Flask, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# In-memory storage for todos
todos = [
    {"id": 1, "text": "Learn JavaScript"},
    {"id": 2, "text": "Learn React"},
    {"id": 3, "text": "Build a project"}
]

# Counter for generating new todo IDs
next_id = 4

@app.route('/todos', methods=['GET'])
def get_todos():
    """Get all todos"""
    return jsonify(todos)

@app.route('/todos', methods=['POST'])
def create_todo():
    """Create a new todo"""
    global next_id
    
    # Get JSON data from request
    data = request.get_json()
    
    # Validate that 'text' field is provided
    if not data or 'text' not in data:
        return jsonify({"error": "Todo text is required"}), 400
    
    # Create new todo
    new_todo = {
        "id": next_id,
        "text": data['text']
    }
    
    # Add to todos list and increment ID counter
    todos.append(new_todo)
    next_id += 1
    
    return jsonify(new_todo), 201


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port, debug=True)