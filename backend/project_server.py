from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
import threading
import time
import random
import paho.mqtt.client as mqtt
import os

BROKER = "127.0.0.1"   
PORT = 1883
TOPIC = "sensors/+"

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST", "localhost") 
DB_PORT = os.getenv("DB_PORT", "5432")


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

socketio = SocketIO(app, cors_allowed_origins="*")
def send_temperature_data():
    while True:
        socketio.sleep(2)
        
        temp1 = round(23.0 + random.uniform(-0.5, 0.5), 1)
        temp2 = round(19.0 + random.uniform(-0.5, 0.5), 1)

        socketio.emit('sensor_update', {'id': '1', 'temperature': temp1, 'humidity': 45})
        socketio.emit('sensor_update', {'id': '2', 'temperature': temp2, 'humidity': 60})

def send_pressure_data():
    while True:
        socketio.sleep(10)
        default_pressure = 1013
        new_pressure = default_pressure + random.uniform(-3.5, 3.5)
        socketio.emit('sensor_update', {'id': '1', 'pressure': new_pressure})

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Połączono z MQTT Brokerem (kod: {rc})")
    client.subscribe(TOPIC)
    print(f"Nasłuchuję na temacie: {TOPIC}")

def on_message(client, userdata, msg):
    try:
        esp_id = msg.topic.split("/")[-1] 
        payload = json.loads(msg.payload.decode('utf-8'))
        payload['id'] = esp_id
        socketio.emit('sensor_update', payload)
        print(f"Przekazano dane z ESP-{esp_id} do Vue: {payload}")
    except Exception as e:
        print(f"Błąd przetwarzania wiadomości MQTT: {e}")


# threading.Thread(target=send_temperature_data, daemon=True).start()
# threading.Thread(target=send_pressure_data, daemon=True).start()
# client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
# client.on_connect = on_connect
# client.on_message = on_message
# client.connect(BROKER, PORT, 60)
# client.loop_start()
# @app.route("/data/temperature")
# def index():
#     return render_template("index.html")


if __name__ in "__main__":
    fake_data = os.getenv("FAKE_DATA","true").lower() in ("true", "1")
    if fake_data:
        socketio.start_background_task(send_temperature_data)
        socketio.start_background_task(send_pressure_data)
    else:
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        client.on_connect = on_connect
        client.on_message = on_message
        client.connect(BROKER, PORT, 60)
        client.loop_start()
            
    socketio.run(app,host="0.0.0.0",debug=True, port=5000,allow_unsafe_werkzeug=True)


