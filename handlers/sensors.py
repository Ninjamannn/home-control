import json
import logging

import falcon

import errors
from database import influx_db
from services.openweather.weather_service import get_weather_data


class SensorDataHandler:
    """
    sensors_data = {
        'sensors_data': [
            {
                'room': 'boiler',
                'type_sensor': 'dht22',
                'type_value': 'temp',
                'value': '100'
            },
            {
                'room': 'boiler',
                'sensor_type': 'ds18b20',
                'value_type': 'temp',
                'value': '100'
            }
        ]
    }
    """

    logger = logging.getLogger(__name__)

    def validate_body(self, request):
        body = request.bounded_stream.read()

        try:
            request_data = json.loads(body)
        except ValueError:
            self.logger.warning('malformed request body', body=str(body))
            raise errors.ValidationError()
        return request_data

    def on_post(self, req, resp):
        try:
            sensors_data = self.validate_body(req)
        except errors.ValidationError:
            resp.status = falcon.HTTP_400
            return

        influx_db.save_sensors_data(sensors_data=sensors_data)
