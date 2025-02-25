from datetime import datetime
from enum import Enum
import json
from json.decoder import JSONDecodeError
import ssl
from typing import NamedTuple, Literal
import urllib.request
from urllib.error import URLError
from config import USE_ROUNDED_COORDS, OPENWEATHER_URL
from geopy.geocoders import Nominatim

Celsius = float


class Coordinates(NamedTuple):
    longitude: float
    latitude: float


def get_coordinates() -> Coordinates:
    latitude = 51.565782
    longitude = 39.121792
    if USE_ROUNDED_COORDS:
        longitude, latitude = map(lambda c: round(c, 4), [longitude, latitude])
    return Coordinates(longitude=longitude, latitude=latitude)


class WeatherType(Enum):
    THUNDERSTORM = "Гроза"
    DRIZZLE = "Изморозь"
    RAIN = "Дождь"
    SNOW = "Снег"
    CLEAR = "Ясно"
    FOG = "Туман"
    CLOUDS = "Облачно"


class Weather(NamedTuple):
    temperature: Celsius
    weather_type: WeatherType
    sunrise: datetime
    sunset: datetime
    city: str


def get_weather(coordinates: Coordinates) -> Weather:
    """Requesrts weather in OpenWeather API and returns it"""
    openweather_response = _get_openweather_response(longitude=coordinates.longitude, latitude=coordinates.latitude)
    weather = _parse_openweater_response(openweather_response)
    return weather


def _get_openweather_response(latitude: float, longitude: float) -> str:
    ssl._create_default_https_context = ssl._create_unverified_context
    url = OPENWEATHER_URL.format(latitude=latitude, longitude=longitude)
    try:
        return urllib.request.urlopen(url).read()
    except URLError:
        print("Program can't get current weather")


def _parse_openweater_response(openweather_response: str) -> Weather:
    try:
        openweather_dict = json.loads(openweather_response)
    except JSONDecodeError:
        print("Program can't get current weather")
    return Weather(
        temperature=_parse_temperature(openweather_dict),
        weather_type=_parse_weather_type(openweather_dict),
        sunrise=_parse_sun_time(openweather_dict, "sunrise"),
        sunset=_parse_sun_time(openweather_dict, "sunset"),
        city=_get_city(coordinates=get_coordinates())
    )


def _parse_temperature(openweather_dict: dict) -> Celsius:
    return round(openweather_dict["main"]["temp"])


def _parse_weather_type(openweather_dict: dict) -> WeatherType:
    try:
        weather_type_id = str(openweather_dict["weather"][0]["id"])
    except (IndexError, KeyError):
        print("Program can't get current weather")
    weather_types = {
        "1": WeatherType.THUNDERSTORM,
        "3": WeatherType.DRIZZLE,
        "5": WeatherType.RAIN,
        "6": WeatherType.SNOW,
        "7": WeatherType.FOG,
        "800": WeatherType.CLEAR,
        "80": WeatherType.CLOUDS
    }
    for _id, _weather_type in weather_types.items():
        if weather_type_id.startswith(_id):
            return _weather_type
    print("Program can't get current weather")


def _parse_sun_time(openweather_dict: dict, time: Literal["sunrise"] | Literal["sunset"]) -> datetime:
    return datetime.fromtimestamp(openweather_dict["sys"][time])


def _get_city(coordinates: Coordinates) -> str:
    geolocator = Nominatim(user_agent="my_unique_app_or_email@example.com")
    location = geolocator.reverse((coordinates.latitude, coordinates.longitude), language='ru')
    if location is not None:
        address = location.raw.get('address', {})
        city = address.get('city') or address.get('town') or address.get(
            'village') or 'Не удалось определить населенный пункт'
        return city
    else:
        return "Не удалось получить данные по координатам"


def format_weather(weather: Weather) -> str:
    """Formats weather data in string"""
    return (
        f"{weather.city}: "
        f"Температура: {weather.temperature}°C, "
        f"{weather.weather_type.value}\n"
        f"Восход: {weather.sunrise.strftime('%H:%M')}\n"
        f"Закат: {weather.sunset.strftime('%H:%M')}\n"
    )


def main_bot(local_lat, local_lon):
    coordinates = Coordinates(local_lon, local_lat)
    weather = get_weather(coordinates)
    return format_weather(weather)


def main():
    coordinates = get_coordinates()
    weather = get_weather(coordinates)
    print(format_weather(weather))


if __name__ == "__main__":
    main()
