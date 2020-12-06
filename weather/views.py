import requests
import json
from django.shortcuts import render, redirect
from weather.models import DayForecast
from bs4 import BeautifulSoup as BSoup


def scrape(request):
    # aquire long/lat.
    ip_data = requests.get("https://ipinfo.io/ip", verify=False)
    ip = ip_data.text.split('\n')[0]
    geo_ip_data = requests.get("https://json.geoiplookup.io/" + ip, verify=False)
    geo_dict = geo_ip_data.json()
    lat = geo_dict['latitude']
    lon = geo_dict['longitude']
    header_info = {"User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html)"}
    url_list = ["https://api.weather.gov/points/",
                # ^ use-age example: https://api.weather.gov/points/{latitude},{longitude}
                "https://darksky.net/forecast/"
                # ^ can also use longitude and latitude in url to get weather data, such as
                # https://darksky.net/{lat},{lon}/us12/en
                ]
    content = requests.get(url_list[1] + str(lat) + ',' + str(lon) + '/us12/en', headers=header_info, verify=False).content
    soup = BSoup(content, "html.parser")
    weather_site = soup.find_all('span', {"class": "summary-high-low"})
    m_forecast = DayForecast()
    m_forecast.weather = weather_site[0].text
    m_forecast.url = "Dark Sky:"
    m_forecast.save()
    content = requests.get(url_list[0] + str(lat) + ',' + str(lon), verify=False)
    content_data = content.json()
    forecast_data = requests.get(content_data['properties']['forecast'])
    forecast = forecast_data.json()
    print(forecast)
    info = forecast['properties']['periods'][0]['detailedForecast']
    m_forecast2 = DayForecast()
    m_forecast2.weather = info
    m_forecast2.url = "National Weather Service:"
    m_forecast2.save()
    return redirect("../")

def forecast_list(request):
    data = DayForecast.objects.all().distinct()[::-1]
    context = {'object_list': data, }
    return render(request, "home.html", context)
