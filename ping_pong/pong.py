from flask import Flask

app = Flask(__name__)

# In-memory counter (will reset when app restarts)
counter = 0
LOG_FILE = '/usr/src/app/files/data.log'
# LOG_FILE = 'data.log'

@app.route('/pingpong', methods=['GET'])
def pingpong():
    global counter
    response = f"pong {counter}"
    line = f"Ping / Pongs: {counter}\n"
    counter += 1
    with open(LOG_FILE, 'a') as f:
        f.write(line)
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)