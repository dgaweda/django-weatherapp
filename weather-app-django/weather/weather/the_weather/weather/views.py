import requests
from django.shortcuts import render
from .models import City
from .forms import CityForm

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=c5bc2cf5da54016e5e50083093aa08f1'

    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()

    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for city in cities:

        r = requests.get(url.format(city)).json()

        city_weather = {# pobieda dane z ogolnodostepnej bazy miast oraz ich pogód
            'city' : city.name,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }

        weather_data.append(city_weather)

    context = {'weather_data' : weather_data, 'form' : form}
    return render(request, 'weather/weather.html', context)
