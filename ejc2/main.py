# 2. Crear una herramienta que permita ejecutar las siguientes tareas:
#     1. Dada una dirección IP o un nombre de dominio, encontrar información relacionada con el propietario de dicho dominio y los registros DNS correspondientes. (Ver librerías disponibles para realizar consultas WHOIS y DNS respectivamente)
#     2. Ejecutar un escaneo con Nmap contra el objetivo y posteriormente, obtener más información del objetivo utilizando Shodan.
#     3. En el caso de encontrar puertos que frecuentemente se relacionan con servidores web (80, 8080, 443) realizar una petición HTTP utilizando el método OPTIONS para determinar si efectivamente, el objetivo es un servidor web y extraer los métodos HTTP soportados.
import argparse
import validators
import sys
import logging
import requests

from lib import (util_whois, util_nmap, util_shodan)

# definimos el argumento a recibir
ap = argparse.ArgumentParser()
ap.add_argument(dest="domain", help="Introduzca un nombre de dominio o una ipv4 valida")
args = ap.parse_args()

# definimos el logger en caso de error
logger = logging.getLogger('logger')
logger.setLevel(logging.DEBUG)

# creamos y asignamos el filehandler al logger
fh = logging.FileHandler('ejc2.log')
fh.setLevel(logging.DEBUG)


def check_http_ports(df, shodan_host: list):
    """Comprobamos si de verdad tiene una pagina http en ese puerto"""
    http_ports = [80, 8080, 443]
    for _, row in df.iterrows():

        if row.hostname and row.port in http_ports:
            url_http = f"http://{row.hostname}:{row.port}"
            r = requests.options(url_http)
            if r.status_code == 400:
                url_http = f"https://{row.hostname}:{row.port}"
                r = requests.options(url_http)
            if r.status_code == 400:
                print(f"\nInformación de {url_http}: No es una pagina http o https\n")
            else:
                print(f"\nInformación de {url_http}:\n")
                print(r.headers)


if __name__ == '__main__':
    domain = args.domain

    if validators.url(domain) or validators.ipv4(domain) or validators.ipv6(domain):
        domain = util_whois.extract_domain(domain)

    if validators.domain(domain):
        dns_info = util_whois.get_dns_domain_info(domain)
        whois_info = util_whois.get_whois(domain)
        df_nmap = util_nmap.basic_scan(dns_info, whois_info)
        shodan_client = util_shodan.ApiShodan(dns_info=dns_info, whois_info=whois_info)
        shodan_host = shodan_client.get_host()

        shodan_client.print_result(shodan_host, "imprimiendo host")

        print("|nComprobamos si son paginas http")
        check_http_ports(df_nmap, shodan_host)
        print("Proceso Finalizado")
    else:
        sys.exit("Introduzca un dominio o una dirección ipv4")
