from django.shortcuts import render
import requests
from django.http import HttpResponse
from bs4 import BeautifulSoup
# Create your views here.

def scrapper(starships):
    starships_url = 'http://starwars.wikia.com/wiki/{0}'
    url_starship = [starships_url.format(star['name'].replace(' ','_')) for star in starships]
    list_star = list()
    for index,url in enumerate(url_starship,start=0):
        req = requests.get(url)
        try:
            soup = BeautifulSoup(req.text,'html.parser')
            imgs = soup.find_all('img',attrs={'class':'pi-image-thumbnail'})
            list_star.append(
                dict(
                    name=starships[index]['name'],
                    url_image=imgs[0]['src']
                )
            )
        except:
            list_star.append(
                dict(
                    name=starships[index]['name'],
                    url_image=''
                )
            )
    return list_star

def index(request,pagina=1):
    # return HttpResponse("<h1>Starships</h1>")
    req = requests.get("https://swapi.co/api/starships/?page={0}".format(pagina))
    if req.status_code == 200:
        starships = scrapper(req.json()['results'])
        print(starships[1])
    else:
        starships = []
    return render(request, 'starships/index.html',{'naves':starships})
