from flask import Flask, render_template, send_from_directory, request, redirect, url_for
from pathlib import Path
import os

app = Flask(__name__)

# Configuration
FILES_DIR = '/usr/src/app/files'

# Hardcoded todos
todos = [
    "Learn JavaScript",
    "Learn React", 
    "Build a project"
]

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

@app.route('/')
def index():
    """Main page displaying the latest image and todos."""
    image_filename = get_latest_image()
    return render_template('index.html', image_filename=image_filename, todos=todos)

@app.route('/files/<filename>')
def serve_image(filename):
    """Serve images from the files directory."""
    return send_from_directory(FILES_DIR, filename)

@app.route('/add_todo', methods=['POST'])
def add_todo():
    """Add a new todo to the list."""
    new_todo = request.form.get('todo', '').strip()
    
    if new_todo and len(new_todo) <= 140:
        todos.append(new_todo)
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port, debug=True)