from flask import Flask, jsonify, request
import json
from datetime import datetime, timedelta

app = Flask(__name__)

x = 0
y = 0
z = 0
last_updated_time = datetime.now()

@app.route('/', methods=['GET', 'POST'])
def handle_health():
    global x
    global y
    global z
    global last_updated_time

    request_size = request.content_length

    # Вы можете использовать размер запроса для выполнения нужных операций
    #print(f"Размер запроса: {request_size} байт")

    if request.method == 'POST':
        data = json.loads(request.data)
        x = data['x']
        y = data['y']
        z = data['z']
        last_updated_time = datetime.now()
        #print(f"Received marker: {x}, {y}, {z}")
        return jsonify({'success': True})

    elif request.method == 'GET':
        current_time = datetime.now()
        if (current_time - last_updated_time) > timedelta(seconds=7):
            if x != 0 or y != 0 or z != 0:
                x = 0
                y = 0
                z = 0
                print("Coordinates set to zero as they haven't changed in 7 seconds.")
        #print(f"Sent marker: {x}, {y}, {z}")
        return jsonify({'x': x, 'y': y, 'z': z})

    else:
        return jsonify({'error': 'Invalid request method'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
