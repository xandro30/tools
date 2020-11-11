# 1. Crear un script en Python que se encargue de imprimir todos los formularios y enlaces de una página web enviada por argumento al programa.
from bs4 import BeautifulSoup
import requests

if __name__ == '__main__':
    url = "https://www.marca.com/"
    r = requests.get(url)
    html = r.content
    print("******************")
    soup = BeautifulSoup(html, 'html.parser')
    form = soup.find_all('form')

    for a in form:
        print(a.get_text())
