from sqlalchemy import text
from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
import threading
import time
import random
import paho.mqtt.client as mqtt
import os
from datetime import datetime

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

class SensorReading(db.Model):
    __tablename__ = 'sensor_readings'
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, primary_key=True)
    esp_id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Float)
    pressure = db.Column(db.Float)
    humidity = db.Column(db.Float)
    tilt = db.Column(db.Float)
    light = db.Column(db.Float)


socketio = SocketIO(app, cors_allowed_origins="*")
def send_temperature_data():
    while True:
        socketio.sleep(2)
        temp1 = round(23.0 + random.uniform(-0.5, 0.5), 1)
        temp2 = round(19.0 + random.uniform(-0.5, 0.5), 1)

        fake_payload = [{'id': '1', 'temperature': temp1, 'humidity': 45},{'id': '2', 'temperature': temp2, 'humidity': 60}]        

        for payload in fake_payload:
            emit_sensors_update(payload)
            save_sensors_reading_to_db(payload)

       

def save_sensors_reading_to_db(payload):
    with app.app_context():
            nowy_odczyt = SensorReading(
                esp_id=payload.get('id'),
                temperature=payload.get('temperature'),
                pressure=payload.get('pressure'),
                humidity=payload.get('humidity'),
                tilt=payload.get('tilt'),
                light=payload.get('light')
            )
            db.session.add(nowy_odczyt)
            db.session.commit()
            print(f"Zapisano odczyt w bazie dla ESP-{payload.get('id')}")

def send_pressure_data():
    while True:
        socketio.sleep(10)
        default_pressure = 1013
        new_pressure = default_pressure + random.uniform(-3.5, 3.5)
        socketio.emit('sensor_update', {'id': '1', 'pressure': new_pressure})

def parse_mqtt_message(msg):
    esp_id_str = msg.topic.split("/")[-1]
    esp_id = int(esp_id_str)
    payload = json.loads(msg.payload.decode('utf-8'))
    payload['id'] = esp_id
    return payload

def emit_sensors_update(payload):
    socketio.emit('sensor_update', payload)
    print(f"Przekazano dane z ESP-{payload['id']} do Vue: {payload}")

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Połączono z MQTT Brokerem (kod: {reason_code})")
    client.subscribe(TOPIC)
    print(f"Nasłuchuję na temacie: {TOPIC}")

def on_message(client, userdata, msg):
    try:
        payload = parse_mqtt_message(msg)
        emit_sensors_update(payload)
        save_sensors_reading_to_db(payload)
    except ValueError:
        print(f"Błąd: Ostatni człon topicu MQTT '{esp_id_str}' nie jest liczbą całkowitą!")
    except json.JSONDecodeError:
        print("Błąd: Otrzymano nieprawidłowy format JSON z MQTT!")
    except Exception as e:
        print(f"Błąd przetwarzania wiadomości MQTT: {e}")

def create_hyper_table():
    with app.app_context():
        db.create_all()
        try:
            db.session.execute(text("SELECT create_hypertable('sensor_readings', 'timestamp', if_not_exists => TRUE);"))
            db.session.commit()
            print("Baza danych gotowa i zoptymalizowana jako Hypertable!")
        except Exception as e:
            db.session.rollback()
            print(f"Info o Hypertable: {e}")

if __name__ in "__main__":
    create_hyper_table()
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


