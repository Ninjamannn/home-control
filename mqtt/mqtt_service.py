from paho.mqtt import client
from decouple import config

from database import influx_db
from utils import log
from .mqtt_errors import MQTT_ERRORS


MQTT_USER = config('MQTT_USER', cast=str)
MQTT_PASS = config('MQTT_PASS', cast=str)
MQTT_HOST = config('MQTT_HOST', cast=str)
MQTT_PORT = config('MQTT_PORT', cast=int)
CLIENT_ID = config('CLIENT_ID', cast=str)


def on_connect(client, userdata, flags, rc):
    log.info(f'Connected with result code: {MQTT_ERRORS[str(rc)]}')
    client.subscribe([('boiler_room/sensors/ds18b20', 0), ('boiler_room/sensors/dht22/#', 0)])


def on_message(client, userdata, msg):
    log.info(f"{msg.topic}: {msg.payload.decode('utf-8')}")
    data = msg.payload.decode('utf-8')
    save_mqtt_data(data, msg.topic)


def on_disconnect(client, userdata, rc):
    """
    loop_stop for resolve extra connections
    """
    if rc != 0:
        log.info(f"Unexpected MQTT disconnection ERROR - {MQTT_ERRORS[str(rc)]}")
        log.info(f"stop extra connections...")


def mqtt_run_service():
    subscriber = client.Client(client_id=CLIENT_ID)  # TODO: change id for prod to CLIENT_ID var.
    subscriber.username_pw_set(MQTT_USER, password=MQTT_PASS)
    subscriber.on_connect = on_connect
    subscriber.on_message = on_message
    subscriber.on_disconnect = on_disconnect
    subscriber.connect_async(MQTT_HOST, MQTT_PORT)
    log.info('mqtt service started')
    # subscriber.loop_start()
    subscriber.loop_forever()


def save_mqtt_data(data, topic):
    if data == 'nan':
        log.error(f'inconsistent data from mqtt: topic - {topic}, data - {data}')
        return None

    room = topic.split('/')[0]
    type_sensor = topic.split('/')[2]

    influx_db.influx_db_client(
        [
            {
                "measurement": "climate",
                "tags": {
                    "room": room,
                    "type_sensor": type_sensor,
                    "type_value": ''
                },
                "fields": {
                    "value": round(float(data), 1)
                }
            }
        ]
    )
