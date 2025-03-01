OPENWEATHER_API = '919e55ddfa6b8731b67dc3f155e6bd65'

OPENWEATHER_URL = (
    "https://api.openweathermap.org/data/2.5/weather?"
    "lat={latitude}&lon={longitude}&"
    "appid=" + OPENWEATHER_API + "&lang=ru&"
    "units=metric"
)


print(type(OPENWEATHER_URL))
print(OPENWEATHER_URL)
