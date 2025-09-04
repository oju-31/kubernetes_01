from flask import Flask
import os

app = Flask(__name__)
LOG_FILE = '/usr/src/app/files/data.log'

@app.route('/')
def read_file():
    try:
        with open(LOG_FILE, 'r') as f:
            content = f.read()
        return f"<pre>{content}</pre>"
    except FileNotFoundError:
        return "File not found"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port)