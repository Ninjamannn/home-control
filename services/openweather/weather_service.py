from decouple import config
from pyowm import OWM


owm = OWM(config('OPEN_WEATHER_API_KEY'))


def get_weather_data() -> dict:
    """
    # w.detailed_status         # 'clouds'
    # w.wind()                  # {'speed': 4.6, 'deg': 330}
    # w.humidity                # 87
    # w.temperature('celsius')  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}
    # w.rain                    # {}
    # w.heat_index              # None
    # w.clouds                  # 75
    """
    mgr = owm.weather_manager()

    observation = mgr.weather_at_place('Minsk,BY')
    w = observation.weather

    weather_temp = w.temperature('celsius').get('temp', 0)
    weather_wind_speed = w.wind().get('speed', 0)
    weather_wind_deg = w.wind().get('deg', 0)

    return dict(
        weather_temp=weather_temp,
        weather_wind_speed=weather_wind_speed,
        weather_wind_deg=weather_wind_deg
    )
