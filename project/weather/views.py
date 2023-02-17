from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages

import requests


parameteres = {
    'appid': 'b01e7608c07f15c54ff9d9b64d478705'
}

def search(request):
    radio = request.GET.get('inlineRadioOptions')
    city_name = request.GET.get('city')

    if not city_name:
        city_name = 'Tashkent'

    if radio == 'option1':
        view_temp = 'metric'
    else:
        view_temp = 'standard'

    parameteres['q'] = city_name
    parameteres['units'] = view_temp
    try:
        req = requests.get(f"https://api.openweathermap.org/data/2.5/weather", params=parameteres).json()

        name = req['name']
        weather = req['weather'][0]['description']
        wind = req['wind']['speed']
        temp = req['main']['temp']
        feels_like = req['main']['feels_like']
        temp_max = req['main']['temp_max']
        temp_min = req['main']['temp_min']
        country = req['sys']['country']

        context = {
            'title': 'Weather',
            'city_name': name,
            'country': country,
            'weather': str(weather).capitalize(),
            'wind': wind,
            'temp': temp,
            'feels_like': feels_like,
            'temp_max': temp_max,
            'temp_min': temp_min,
        }

        return render(request, 'weather/index.html', context)
    except:
        messages.error(request, "The city name was entered incorrectly!")
        return redirect('search')