from flask import Flask, render_template, send_from_directory
from pathlib import Path
import os

app = Flask(__name__)

# Configuration
FILES_DIR = '/usr/src/app/files'


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
    """Main page displaying the latest image."""
    image_filename = get_latest_image()
    return render_template('index.html', image_filename=image_filename)

@app.route('/image/<filename>')
def serve_image(filename):
    """Serve image files from the files directory."""
    return send_from_directory(FILES_DIR, filename)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port, debug=True)
