# 1. Crear un script en Python que se encargue de imprimir todos los formularios y enlaces de una página web enviada por argumento al programa.
from bs4 import BeautifulSoup
import requests
import argparse
import validators
import sys
import traceback
import logging

# definimos el argumento a recibir
ap = argparse.ArgumentParser()
ap.add_argument(dest="url", help="Introduzca una url valida")
args = ap.parse_args()

# definimos el logger en caso de error
logger = logging.getLogger('logger')
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler('ejc1.log')
fh.setLevel(logging.DEBUG)

logger.addHandler(fh)

if __name__ == '__main__':
    url = args.url

    # comprobamos si es una url valida
    if not validators.url(url):
        sys.exit("La url introducida, no es valida introduzca una url con el siguiente formato: 'http://domain.com'")

    try:
        logger.info("accediendo al contenido de la siguiente url: {url}".format(url=url))
        r = requests.get(url)
    except:
        logger.error("Error al acceder a la siguiente url: {url}".format(url=url))
        tb = sys.exc_info()[2]
        error_message = str(sys.exc_info()[1])
        tbinfo = traceback.format_tb(tb)[0]
        pymsg = "PYTHON ERRORS:\nTraceback info:\n {tbinfo}\n Error Info: {error}".format(tbinfo=tbinfo, error=error_message)
        logger.error(pymsg)
        sys.exit("No se a podido acceder al dominio solicitado")

    # comprobamos que la petición a sido correcta
    if r.status_code != 200:
        sys.exit("El recurso que quiere acceder, no se encuentra disponible")

    html = r.content

    soup = BeautifulSoup(html, 'html.parser')
    list_forms = soup.find_all('form')
    list_a = soup.find_all('a')

    if len(list_forms) > 0:
        print("*****************************")
        print("*Imprimiendo los formularios*")
        print("*****************************")
        for form in list_forms:
            print(form)
    else:
        print("la página {url} no contiene formularios".format(url=url))

    if len(list_a) > 0 :
        print("*************************")
        print("*Imprimiendo los enlaces*")
        print("*************************")
        for a in list_a:
            print(a)
    else:
        print("La página {} no contiene enlaces".format(url))
