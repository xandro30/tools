# 2. Crear una herramienta que permita ejecutar las siguientes tareas:
#     1. Dada una dirección IP o un nombre de dominio, encontrar información relacionada con el propietario de dicho dominio y los registros DNS correspondientes. (Ver librerías disponibles para realizar consultas WHOIS y DNS respectivamente)
#     2. Ejecutar un escaneo con Nmap contra el objetivo y posteriormente, obtener más información del objetivo utilizando Shodan.
#     3. En el caso de encontrar puertos que frecuentemente se relacionan con servidores web (80, 8080, 443) realizar una petición HTTP utilizando el método OPTIONS para determinar si efectivamente, el objetivo es un servidor web y extraer los métodos HTTP soportados.
import requests
import argparse
import validators
import sys
import traceback
import logging
import utilities

# definimos el argumento a recibir
ap = argparse.ArgumentParser()
ap.add_argument(dest="param", help="Introduzca un nombre de dominio o una ipv4 valida")
args = ap.parse_args()

# definimos el logger en caso de error
logger = logging.getLogger('logger')
logger.setLevel(logging.DEBUG)

# creamos y asignamos el filehandler al logger
fh = logging.FileHandler('ejc2.log')
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)

if __name__ == '__main__':
    param = args.param

    if validators.url(param) or validators.ipv4(param) or validators.ipv6(param):
        param = utilities.extract_domain(param)

    if validators.domain(param):
        dns_info = utilities.get_dns_domain_info(param)
        whois_info = utilities.get_whois(param)
    else:
        sys.exit("Introduzca un dominio o una dirección ipv4")
