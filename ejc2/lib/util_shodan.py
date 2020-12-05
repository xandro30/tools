from shodan import Shodan
import shodan.stream as Stream
import os
import sys
import sqlite3



class ApiShodan(Shodan):
    """api de shodan"""

    def __init__(self,api_key: str, dns_info: dict, whois_info: dict):
        """override shodan init"""
        #api_key = os.environ.get('SHODAN_API_KEY', None)
        api_key = api_key
        if api_key is None:
            sys.exit("No tiene la api key de shodan entre sus variables de entorno, por favor agregela si desea continuar.")
        Shodan.__init__(self, key=api_key)
        self.dns_info = dns_info
        self.whois_info = whois_info
        account_status = self.info()
        print(f"Shodan plan account {account_status['plan']}")
        print(f"Dispone de {account_status['usage_limits']['scan_credits']} scans")
        print(f"Dispone de {account_status['usage_limits']['query_credits']} query_credits")
        print(f"Dispone de {account_status['usage_limits']['monitored_ips']} ips a monitorizar")

    def conn_sqlite3(self, db="shodan.db") -> sqlite3.Cursor:
        """return cursor to sqlite3"""
        conn = sqlite3.connect(db)
        return conn.cursor()

    def get_host(self) -> dict:
        """Devuelve todos los servicios de la ip encontrada"""
        ip = self.dns_info['a']['name_server']
        return self.host(ips=ip)

    def check_scans(self) -> dict:
        """Comprueba si hay algun scan terminado y lo recupera en caso de ser correcto"""
        status_scans = self.scans()
        finish_scans = [scan for scan in status_scans['matches'] if scan['status'] == "DONE"]
        if len(finish_scans) > 0:
            print(f"Hay {len(finish_scans)} scans terminados")
        else:
            print("No tiene scans aun terminados")
        print(status_scans)
        return finish_scans

    def start_scan(self) -> dict:
        """Inicia un scan de shodan"""
        ip = self.dns_info['a']['name_server']
        #scann_data = self.scan(ips=ip)
        print("se ha agregado su scann a la cola")
        finish_scans = self.check_scans()
        return finish_scans




