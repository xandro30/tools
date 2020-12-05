import nmap
import pandas as pd
from io import StringIO


def basic_scan(dns_info: dict, whois_info: dict):
    """Lanza un scanneo basico de nmap"""
    # TODO: revisar por que no muestra resultados, algo esta mal con la instalacion de nmap resolver
    nm = nmap.PortScanner()
    hosts = f"{dns_info['a']['name_server']} {whois_info['domain']} {whois_info['whois_server']}"
    scanner = nm.scan(hosts=hosts, arguments="-sV -n -A -T5")
    a = nm.csv()
    df = pd.read_csv(StringIO(a), sep=";")

    print(df)


