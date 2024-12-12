from tkinter import *
from tkinter import messagebox
from configparser import ConfigParser
import requests
from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *


url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'

config_file = 'config.ini'
config = ConfigParser()
config.read(config_file)
api_key = config['api_key']['key']

def get_weather(city):
    result = requests.get(url.format(city, api_key))
    if result:
        json = result.json()
        city = json['name']
        country = json['sys']['country']
        temp_kelvin = json['main']['temp']
        temp_celsius = temp_kelvin - 273.15
        temp_fahrenheit = (temp_kelvin - 273.15) * 9 / 5 + 32
        icon = json['weather'][0]['icon']
        weather = json['weather'][0]['main']
        description = json['weather'][0]['description']
        # more weather details
        humidity = json['main']['humidity']
        pressure = json['main']['pressure']
        wind_speed = json['wind']['speed']
        feels_like = json['main']['feels_like'] - 273.15
        
        final = (city, country, temp_celsius, temp_fahrenheit, icon, weather, 
                description, humidity, pressure, wind_speed, feels_like)
        return final
    else:
        return None

def search():
    global img
    city = city_text.get()
    weather = get_weather(city)
    if weather:
        # Update main weather info
        location_lbl.config(text='{}, {}'.format(weather[0], weather[1]))
        img['file'] = 'weather_icons/{}.png'.format(weather[4])
        temp_lbl.config(text='{:.1f}°C | {:.1f}°F'.format(weather[2], weather[3]))
        weather_lbl.config(text=weather[5])
        description_lbl.config(text=weather[6].capitalize())
        
        # Update additional weather details with better formatting
        humidity_lbl.configure(text=f'💧 Humidity\n{weather[7]}%')
        pressure_lbl.configure(text=f'🌡️ Pressure\n{weather[8]} hPa')
        wind_lbl.configure(text=f'💨 Wind Speed\n{weather[9]:.1f} m/s')
        feels_like_lbl.configure(text=f'🌡️ Feels Like\n{weather[10]:.1f}°C')
    else:
        messagebox.showerror('Error', 'Cannot find city {}'.format(city))

# Create the main window using ttkbootstrap
app = ttk.Window(themename="darkly")
app.title("Weather App")
app.geometry("700x800")
app.minsize(700, 800)

# Create main frame with modern styling
main_frame = ttk.Frame(app, padding="10")
main_frame.pack(fill=BOTH, expand=True)

# Search Frame with modern styling
search_frame = ttk.Frame(main_frame)
search_frame.pack(pady=10, fill=X)

city_text = StringVar()
city_entry = ttk.Entry(
    search_frame,
    textvariable=city_text,
    font=('Segoe UI', 12),
    width=30
)
city_entry.pack(side=LEFT, padx=5, fill=X, expand=True)

search_btn = ttk.Button(
    search_frame,
    text='Search Weather',
    command=search,
    style='primary.TButton',
    cursor='hand2'
)
search_btn.pack(side=LEFT, padx=5)

# Results Frame with modern styling
results_frame = ttk.Frame(main_frame)
results_frame.pack(pady=10, fill=BOTH, expand=True)

# Location and main weather info
location_lbl = ttk.Label(
    results_frame,
    text='Enter a city name',
    font=('Segoe UI', 20, 'bold'),
    justify=CENTER
)
location_lbl.pack(pady=5)

img = PhotoImage(file="")
Image = ttk.Label(results_frame, image=img)
Image.pack(pady=10)

temp_lbl = ttk.Label(
    results_frame,
    text='',
    font=('Segoe UI', 36),
    justify=CENTER
)
temp_lbl.pack(pady=5)

weather_lbl = ttk.Label(
    results_frame,
    text='',
    font=('Segoe UI', 18),
    justify=CENTER
)
weather_lbl.pack()

description_lbl = ttk.Label(
    results_frame,
    text='',
    font=('Segoe UI', 14),
    justify=CENTER
)
description_lbl.pack(pady=5)

# Update the details frame section with better styling
details_frame = ttk.LabelFrame(results_frame, text="Weather Details", padding=10)
details_frame.pack(pady=10, fill=X)

# Create two columns for weather details with better spacing
left_details = ttk.Frame(details_frame)
left_details.pack(side=LEFT, expand=True, padx=10)

right_details = ttk.Frame(details_frame)
right_details.pack(side=RIGHT, expand=True, padx=10)

# Left column details with initial text
humidity_lbl = ttk.Label(
    left_details,
    text='💧 Humidity\n--',
    font=('Segoe UI', 11),
    justify=CENTER
)
humidity_lbl.pack(pady=5)

pressure_lbl = ttk.Label(
    left_details,
    text='🌡️ Pressure\n--',
    font=('Segoe UI', 11),
    justify=CENTER
)
pressure_lbl.pack(pady=5)

# Right column details with initial text
wind_lbl = ttk.Label(
    right_details,
    text='💨 Wind Speed\n--',
    font=('Segoe UI', 11),
    justify=CENTER
)
wind_lbl.pack(pady=5)

feels_like_lbl = ttk.Label(
    right_details,
    text='🌡️ Feels Like\n--',
    font=('Segoe UI', 11),
    justify=CENTER
)
feels_like_lbl.pack(pady=5)

# Bind Enter key
app.bind('<Return>', lambda event: search())

app.mainloop()