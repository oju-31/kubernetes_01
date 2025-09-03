from flask import Flask

app = Flask(__name__)

# In-memory counter (will reset when app restarts)
counter = 0

@app.route('/pingpong', methods=['GET'])
def pingpong():
    global counter
    response = f"pong {counter}"
    counter += 1
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)