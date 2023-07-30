from flask import Flask, jsonify, request
import json
from datetime import datetime, timedelta

app = Flask(__name__)

x = 0
y = 0
z = 0
server = 'nil'
request_frequency = 3
last_updated_time = datetime.now()

@app.route('/', methods=['GET', 'POST'])
def handle_health():
    global x
    global y
    global z
    global server
    global request_frequency

    global last_updated_time


    if request.method == 'POST':
        data = json.loads(request.data)
        x = data['x']
        y = data['y']
        z = data['z']
        server = data['server']
        try:
            request_frequency = data['request_frequency']
        except KeyError:
            pass
        last_updated_time = datetime.now()
        return jsonify({'success': True})

    elif request.method == 'GET':
        current_time = datetime.now()
        if (current_time - last_updated_time) > timedelta(seconds=20):
            if x != 0 or y != 0 or z != 0:
                x = 0
                y = 0
                z = 0
                server = 'nil'
                print("Coordinates set to zero as they haven't changed in 20 seconds.")
        return jsonify({'x': x, 'y': y, 'z': z, 'server' : server, 'request_frequency' : request_frequency})

    else:
        return jsonify({'error': 'Invalid request method'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
