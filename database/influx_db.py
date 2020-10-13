from influxdb import InfluxDBClient
from decouple import config


influx_db = InfluxDBClient(
    username=config('INFLUXDB_ADMIN_USER'),
    password=config('INFLUXDB_ADMIN_PASSWORD'),
    database=config('INFLUXDB_DB')
)

# influx_db.create_database('db0')
