import requests

api_key = "a232d14d70fd83a64219cdb05d95a338"

def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)

    return response  # return the full response so main.py can decide
