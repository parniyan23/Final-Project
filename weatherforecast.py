# This app displayes weather forecast of next 7 days of any city.
#add code here

import requests, json, webbrowser
# from datetime import datetime
import time
from geopy.geocoders import Nominatim

BASE_URL = "https://api.openweathermap.org/data/2.5/onecall?"
# BASE_URL = "https://api.openweathermap.org/data/2.5/onecall?lat=47.6038321&lon=-122.3300624&exclude=current,minutely,hourly&appid=42ab37bb7f1be9f335f08fe5a480ed8c&units=imperial"
IMAGE_URL = "https://openweathermap.org/img/wn/"
API_KEY = "42ab37bb7f1be9f335f08fe5a480ed8c"

# method to convert time in millis to date
def get_date(date):
   return time.strftime('%Y-%m-%d', time.localtime(date))

def get_date_time(date):
   return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(date))


def get_lat_long(city):
   geolocator = Nominatim(user_agent="Parniyan")
   location = geolocator.geocode(city)
   return location

daily = []
date_list = []
temp_daily = []
icon = []

def get_weather_information(lat, long):

   URL = BASE_URL + "lat=" + lat + "&lon=" + long + "&exclude=current,minutely,hourly" + "&appid=" + API_KEY + "&units=imperial"
   weather_info = {}
   try:
      response = requests.get(URL)
      if response.status_code == 200:
         # getting data in the json format
         data = response.json()
         #print(data)
         global temp_daily
         global icon
         global date_list
         daily = data['daily']
         for i in range (7):
            date = daily[i]['dt']
            print(get_date(date))
            date_list.append(get_date(date))
            temp_daily.append(daily[i]['temp'])
            icon_id = daily[i]['weather'][0]['icon']
            image = IMAGE_URL + icon_id + ".png"
            icon.append(image)
            print(daily[i]['temp'])

         # alerts = data['alerts']
         # for alert in alerts:
         #    print('Alert event')
         #    print(alert['event'])
         #    date_time_start = get_date_time(alert['start'])
         #    print(date_time_start)
         #    date_time_end = get_date_time(alert['end'])
         #    print(date_time_end)
      else:
         print("Error in the HTTP request")
         print(str(response))
         return None
   except Exception as e:
      print("Error trying to gather weather information from OpenWeather Api.")
      print(str(e))
      return None

# print("Please enter latitude and longitude of the place:")
# lat = input("Please enter latitude:\n")
# long = input("Please enter longitude:\n")
city = input("Please enter city name:\n")

location = get_lat_long(city)
# print(location.address)
# print((location.latitude, location.longitude))


get_weather_information(str(location.latitude), str(location.longitude))

with open("weather-forecast.html","w") as f:
    f.write("<html><head><title>Weather forecast for next 7 days along with any alerts</title></head>")
    f.write("""<style>body{font-family:sans-serif;} 
              tr.user td{border-top: 1px #888 dashed;} 
              .count{text-align:right}</style>""")
    f.write("<header><h1>Weather forecast for {city}</h1></header>".format(city = city))
    f.write("<body>\n<table cellpadding=10 cellspacing=10>")
    f.write("<tr><td>Date</td><td>Day</td><td>Min</td><td>Max</td><td>Night</td><td>Evening</td><td>Morning</td></tr>")
    for i in range(7):
        f.write("<tr><td>{date}</td><td>{daily}</td><td>{min}</td><td>{max}</td><td>{night}</td><td>{eve}</td><td>{morn}</td><td><img src={photo_url} width='150' height='150'/></td></tr>".format(date = date_list[i], daily=temp_daily[i]['day'], min=temp_daily[i]['min'], max=temp_daily[i]['max'], night=temp_daily[i]['night'], eve=temp_daily[i]['eve'], morn=temp_daily[i]['morn'], photo_url= icon[i]))
    f.write("</table></body>")
