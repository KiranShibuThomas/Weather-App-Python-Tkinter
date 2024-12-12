from tkinter import *
from configparser import ConfigParser
import requests


url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'

config_file = 'config.ini'
config = ConfigParser()
config.read(config_file)
api_key = config['api_key']['key']

def get_weather(city):
    result = requests.get(url,format(city, api_key))
    if result:
        print(result.content)
    else:
        return None
    
    
get_weather('london')
    
    



def search():
    pass

app = Tk()
app.title("Weather App")
app.geometry("700x350")

city_text = StringVar()
city_entry = Entry(app, textvariable=city_text)
city_entry.pack()


search_btn = Button(app, text='Search Weather', width = 12, command=search)
search_btn.pack()

location_lbl = Label(app, text='location', font = ('bold',20))
location_lbl.pack()

image  = Label(app, bitmap ='')
image.pack()

temp_lbl = Label(app, text='')
temp_lbl.pack()

weather_lbl = Label(app,text='')
weather_lbl.pack()


app.mainloop()