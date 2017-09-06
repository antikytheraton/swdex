from django.shortcuts import render
import requests
from django.http import HttpResponse
from bs4 import BeautifulSoup
# Create your views here.

def scrapper(planets):
    worlds_url = 'http://starwars.wikia.com/wiki/{0}'
    url_planet = [worlds_url.format(plan['name'].replace(' ','_')) for plan in planets]
    list_plan = list()
    for index,url in enumerate(url_planet,start=0):
        req = requests.get(url)
        try:
            soup = BeautifulSoup(req.text,'html.parser')
            imgs = soup.find_all('img',attrs={'class':'pi-image-thumbnail'})
            list_plan.append(
                dict(
                    name=planets[index]['name'],
                    url_image=imgs[0]['src']
                )
            )
        except:
            list_plan.append(
                dict(
                    name=planets[index]['name'],
                    url_image=''
                )
            )
    return list_plan

def index(request,pagina=1):
    # return HttpResponse("<h1>Planets</h1>")
    req = requests.get("https://swapi.co/api/planets/?page={0}".format(pagina))
    if req.status_code == 200:
        planets = scrapper(req.json()['results'])
    else:
        planets = []
    return render(request, 'planets/index.html',{'planetas':planets})