import requests
from customtkinter import *
from PIL import Image
from cityList import *


def get_city_id(input_city):
    city_id = "6094817"
    for i in city_list:
        if input_city.lower() == i[0]:
            city_id = i[1]
    return city_id

def get_weather_response(city_id, api):
    apiurl = f'''http://api.openweathermap.org/data/2.5/weather?id={city_id}&appid={api}&units=metric'''
    response = requests.get(apiurl)
    return response


#BASE = "/Users/bisheralmazloum/Desktop/WeatherAPP/"

def get_image_for_condition(condition):
    cond = (condition or "").lower()

    rules = [
        (("light rain",), "rainy.jpeg"),
        (("thunder storm", "thunder"), "thunderstorm.png"),
        (("overcast clouds", "broken clouds", "few clouds"), "cloudy.jpg"),
        (("clear sky", "sunny", "sun"), "sunny.png"),
        (("snowy", "snow"), "snowy.png"),
        (("haze",), "haze.png"),
        (("mist",), "rainy.jpeg"),
        (("rain",), "rainy.jpeg"),
    ]

    filename = "snowy.png"  #default
    for keys, img in rules:
        if any(k in cond for k in keys):
            filename = img
            break

    return Image.open(filename)
