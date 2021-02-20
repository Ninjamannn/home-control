from influxdb import InfluxDBClient
from decouple import config


influx_db_client = InfluxDBClient(
    username=config('INFLUXDB_ADMIN_USER'),
    password=config('INFLUXDB_ADMIN_PASSWORD'),
    database=config('INFLUXDB_DB')
)


def save_sensors_data(sensors_data: dict):
    for sensor in sensors_data['sensors_data']:
        influx_db_client.write_points(
            [
                {
                    "measurement": "climate",
                    "tags": {
                        "room": sensor['room'],
                        "type_sensor": sensor['sensor_type'],
                        "type_value": sensor['value_type']
                    },
                    "fields": {
                        "value": round(float(sensor['value']), 1)
                    }
                }
            ]
        )


def save_weather_data(weather_data: dict):
    for measurement_type, value in weather_data.items():
        influx_db_client.write_points(
            [
                {
                    "measurement": "weather",
                    "tags": {
                        'measurement_type': measurement_type,
                    },
                    "fields": {
                        "value": float(value)
                    }
                }
            ]
        )

# influx_db.create_database('db0')
