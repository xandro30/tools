# 2. Crear una herramienta que permita ejecutar las siguientes tareas:
#     1. Dada una dirección IP o un nombre de dominio, encontrar información relacionada con el propietario de dicho dominio y los registros DNS correspondientes. (Ver librerías disponibles para realizar consultas WHOIS y DNS respectivamente)
#     2. Ejecutar un escaneo con Nmap contra el objetivo y posteriormente, obtener más información del objetivo utilizando Shodan.
#     3. En el caso de encontrar puertos que frecuentemente se relacionan con servidores web (80, 8080, 443) realizar una petición HTTP utilizando el método OPTIONS para determinar si efectivamente, el objetivo es un servidor web y extraer los métodos HTTP soportados.
import argparse
import validators
import sys
import logging
from lib import (util_whois, util_nmap, util_shodan)

# definimos el argumento a recibir
ap = argparse.ArgumentParser()
ap.add_argument(dest="param", help="Introduzca un nombre de dominio o una ipv4 valida")
ap.add_argument(dest="api_key", help="Introduzca la api key de shodan a utilizar")
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
    api_key = args.api_key

    if validators.url(param) or validators.ipv4(param) or validators.ipv6(param):
        param = util_whois.extract_domain(param)

    if validators.domain(param):
        dns_info = util_whois.get_dns_domain_info(param)
        whois_info = util_whois.get_whois(param)
        util_nmap.basic_scan(dns_info, whois_info)
        shodan_client = util_shodan.ApiShodan(api_key=api_key, dns_info=dns_info, whois_info=whois_info)
        info_shodan = shodan_client.get_host()
        result_scan = shodan_client.start_scan()
        print(info_shodan)
        print(result_scan)

        print("Finalizado")
    else:
        sys.exit("Introduzca un dominio o una dirección ipv4")
