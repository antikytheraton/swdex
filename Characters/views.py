from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
# Create your views here.

def scrapper(characters):
    wookie_url = "http://starwars.wikia.com/wiki/{0}"
    url_character = [wookie_url.format(char['name'].replace(' ','_')) for char in characters]
    list_char = list()
    for index,url in enumerate(url_character,start=0):
        req = requests.get(url)
        try:
            soup = BeautifulSoup(req.text,'html.parser')
            imgs = soup.find_all('img',attrs={'class':'pi-image-thumbnail'})
            list_char.append(
                dict(
                    name=characters[index]['name'],
                    url_image=imgs[0]['src']
                )
            )
        except:
            list_char.append(
                dict(
                    name=characters[index]['name'],
                    url_image=''
                )
            )
    return list_char

def index(request,pagina=1):
    req = requests.get("http://swapi.co/api/people/?page={0}".format(pagina))
    if req.status_code == 200:
        characters = scrapper(req.json()['results'])
    else:
        characters = []
    return render(request,'characters/index.html',{'personajes':characters})
