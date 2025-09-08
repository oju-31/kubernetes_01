from flask import Flask, jsonify

app = Flask(__name__)

# In-memory counter (will reset when app restarts)
counter = 0

@app.route('/pingpong', methods=['GET'])
def pingpong():
    global counter
    response = f"pong {counter}"
    line = f"Ping / Pongs: {counter}\n"
    counter += 1
    return response

@app.route('/pings', methods=['GET'])
def get_pings():
    """Return the current ping count as JSON"""
    return jsonify({"pings": counter})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)