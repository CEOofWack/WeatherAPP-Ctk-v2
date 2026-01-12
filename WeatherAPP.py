
from customtkinter import *
from PIL import Image
from displayWeather import *
import os

API = os.getenv('OPENWEATHER_API_KEY', 'your_api_key_here')


app = CTk()
app.title('WeatherAPP')
app.geometry('520x545')
app._set_appearance_mode("dark")
app.configure(fg_color="#0B1220")



title_label = CTkLabel(app, text='WeatherAPP™', font=('Arial', 30, 'bold'), text_color="#E5E7EB")

msg_label = CTkLabel(app, text="", text_color="#E5E7EB", font=('Arial', 18, 'bold'), fg_color="#0F172A", corner_radius=14)
temp_label = CTkLabel(app, text="", text_color="#E5E7EB", font=('Arial', 16), fg_color="#0F172A", corner_radius=14)
feels_temp_label = CTkLabel(app, text="", text_color="#E5E7EB", font=('Arial', 16), fg_color="#0F172A", corner_radius=14)
condition_label = CTkLabel(app, text="", text_color="#E5E7EB", font=('Arial', 16), fg_color="#0F172A", corner_radius=14)
wind_label = CTkLabel(app, text="", text_color="#E5E7EB", font=('Arial', 16), fg_color="#0F172A", corner_radius=14)
alert_label = CTkLabel(app, text="", text_color="#E5E7EB", font=('Arial', 16), fg_color="#0F172A", corner_radius=14)

msg_label2 = CTkLabel(app, text="Select city (press Enter):", text_color="#94A3B8", font=('Arial', 16, 'bold'))


name_entry = CTkEntry(
    app,
    font=('Arial', 18, 'bold'),
    corner_radius=12,
    fg_color="#0F172A",
    text_color="#E5E7EB",
    border_color="#1F2A44",
    placeholder_text="Ottawa / London / Tokyo...",
    height=44
)


c_img = CTkImage(light_image=Image.open('snowy.png'), size=(120, 120))
image_label = CTkLabel(app, image=c_img, text="")
image_label.pack(pady=(18, 10))


def update_weather(event):
 

    input_city = name_entry.get()

    city_id = get_city_id(input_city)

    response = get_weather_response(city_id, API)

    try:
      if response.status_code == 200:
        data = response.json()
        cityname = data['name']
        temperature = data['main']['temp']
        feels_like = data['main']['feels_like']
        condition = data['weather'][0]['description']
        windspeed = data['wind']['speed']
        alert = data.get('alerts')


        print(f"Weather for {cityname}")
        print("Temperature:", temperature)
        print(f"Feels like: {feels_like}")
        print("Wind speed", windspeed)
        print("Condition:", condition)
        print(data)


        msg_label.configure(text=f"Weather for {cityname}: ", font=('Arial', 20, 'bold'))
        temp_label.configure(text=f"Temperature: {temperature}°C", font=('Arial', 16))
        feels_temp_label.configure(text=f"Feels like: {feels_like}°C", font=('Arial', 16))
        condition_label.configure(text=f"Condition: {condition}", font=('Arial', 16))
        wind_label.configure(text=f"Wind speed: {windspeed}m/s", font=('Arial', 16))
        alert_label.configure(text=f"Weather alerts: {alert}", font=('Arial', 16))


        c_img.configure(light_image=get_image_for_condition(condition))
        image_label.configure(image=c_img)


    except Exception as e:
        print(f"Failed to fetch weather information. Error: {e}")
        return



name_entry.bind('<Return>', lambda event: update_weather(event))


update_weather(None)


title_label.pack(pady=(15, 8))
msg_label.pack(pady=6, padx=20, fill="x")
temp_label.pack(pady=6, padx=20, fill="x")
feels_temp_label.pack(pady=6, padx=20, fill="x")
condition_label.pack(pady=6, padx=20, fill="x")
wind_label.pack(pady=6, padx=20, fill="x")
alert_label.pack(pady=6, padx=20, fill="x")
msg_label2.pack(pady=(10, 6))
name_entry.pack(pady=(0, 18), padx=20, fill="x")


app.mainloop()
