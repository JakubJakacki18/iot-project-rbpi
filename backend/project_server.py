# import paho.mqtt.client as mqtt

# BROKER = "192.168.4.1"   
# PORT = 1883
# TOPIC = "RPI/status"

# def on_connect(client, userdata, flags, reason_code, properties):
#     print("Połączono z brokerem, kod:", reason_code)
#     client.publish(TOPIC, "HELLO")
#     client.subscribe("RPI/status")

# def on_message(client, userdata, msg):
#     print(f"Odebrano wiadomość z {msg.topic}: {msg.payload.decode()}")

# client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
# client.on_connect = on_connect
# client.on_message = on_message
# client.connect(BROKER, PORT, 60)
# client.loop_forever()
from flask import Flask, render_template
from flask_socketio import SocketIO
import threading
import time
import random
import paho.mqtt.client as mqtt

BROKER = "127.0.0.1"   
PORT = 1883
TOPIC = "sensors/+"

app = Flask(__name__)
# CORS(app)

socketio = SocketIO(app, cors_allowed_origins="*")
def send_temperature_data():
    while True:
        socketio.sleep(2)
        
        temp1 = round(23.0 + random.uniform(-0.5, 0.5), 1)
        temp2 = round(19.0 + random.uniform(-0.5, 0.5), 1)

        socketio.emit('sensor_update', {'id': '1', 'temp': temp1, 'humidity': 45})
        socketio.emit('sensor_update', {'id': '2', 'temp': temp2, 'humidity': 60})

def send_pressure_data():
    while True:
        socketio.sleep(10)
        default_pressure = 1013
        new_pressure = default_pressure + random.uniform(-3.5, 3.5)
        socketio.emit('pressure_update', {'id': '1', 'pressure': new_pressure})

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
    socketio.start_background_task(send_temperature_data)
    
    socketio.run(app, debug=True, port=5000)


