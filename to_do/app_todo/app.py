from flask import Flask, render_template, send_from_directory, request, redirect, url_for, jsonify
from pathlib import Path
import os
import requests

app = Flask(__name__)

# Configuration
FILES_DIR = '/usr/src/app/files'
TODO_API_BASE_URL = 'http://todo-svc:2345' 

def get_latest_image():
    """Get the most recent image file from the files directory."""
    try:
        files_path = Path(FILES_DIR)
        if not files_path.exists():
            return None
        
        # Find all image files
        image_files = list(files_path.glob("image_*.jpg"))
        if not image_files:
            return None
        
        # Return the most recent one
        latest_image = max(image_files, key=os.path.getmtime)
        return latest_image.name
    except Exception:
        return None

def get_todos_from_api():
    """Fetch todos from the backend API."""
    try:
        response = requests.get(f'{TODO_API_BASE_URL}/todos', timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            # Fallback to default todos if API is not available
            return [{"id": 1, "text": "Learn Noresponse"}]
    except requests.exceptions.RequestException:
        # Fallback to default todos if API is not available
        return [{"id": 1, "text": "Learn RequestException"}]

def add_todo_to_api(todo_text):
    """Add a new todo via the backend API."""
    try:
        response = requests.post(
            f'{TODO_API_BASE_URL}/todos',
            json={"text": todo_text},
            timeout=5
        )
        return response.status_code == 201
    except requests.exceptions.RequestException:
        return False

@app.route('/')
def index():
    """Main page displaying the latest image and todos."""
    image_filename = get_latest_image()
    todos = get_todos_from_api()
    return render_template('index.html', image_filename=image_filename, todos=todos)

@app.route('/add_todo', methods=['POST'])
def add_todo():
    """Add a new todo via API."""
    todo_text = request.form.get('todo', '').strip()
    
    if not todo_text:
        flash('Please enter a todo item', 'error')
    elif len(todo_text) > 140:
        flash('Todo must be 140 characters or less', 'error')
    else:
        success = add_todo_to_api(todo_text)
        if success:
            flash(f'Todo "{todo_text}" added successfully!', 'success')
        else:
            flash('Failed to add todo. Please try again later.', 'error')
    
    return redirect(url_for('index'))

@app.route('/api/todos', methods=['GET'])
def api_get_todos():
    """API endpoint to get todos (proxy to backend)."""
    todos = get_todos_from_api()
    return jsonify(todos)

@app.route('/api/todos', methods=['POST'])
def api_add_todo():
    """API endpoint to add todo (proxy to backend)."""
    data = request.get_json()
    
    if not data or 'text' not in data:
        return jsonify({"error": "Todo text is required"}), 400
    
    success = add_todo_to_api(data['text'])
    
    if success:
        return jsonify({"message": "Todo added successfully"}), 201
    else:
        return jsonify({"error": "Failed to add todo"}), 500

@app.route('/files/<filename>')
def serve_image(filename):
    """Serve images from the files directory."""
    return send_from_directory(FILES_DIR, filename)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port, debug=True)