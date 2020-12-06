from shodan import Shodan


class ApiShodan(Shodan):
    """api de shodan"""

    def __init__(self, dns_info: dict, whois_info: dict):
        """override shodan init"""
        #self.api_key = "WwX00Z0Kw8mVZMxI8bqVhIiPqcHYeP6w"
        self.api_key = "2FxUy9zTW5xsuISKPbImePPqc4b7Cn8o"
        self.dns_info = dns_info
        self.whois_info = whois_info
        Shodan.__init__(self, key=self.api_key)
        account_status = self.info()
        
        print("\n********************")
        print("Shodan info:")
        print("********************\n")

        print(f"Shodan plan account {account_status['plan']}")
        print(f"Dispone de {account_status['usage_limits']['scan_credits']} scans")
        print(f"Dispone de {account_status['usage_limits']['query_credits']} query_credits")
        print(f"Dispone de {account_status['usage_limits']['monitored_ips']} ips a monitorizar")

    def get_host(self) -> dict:
        """Devuelve todos los servicios de la ip encontrada"""
        info = []
        for ip in self.dns_info['A']:
            info.append(self.host(ips=ip, history=False, minify=True))
        return info

    def print_result(self, info: list, title) -> None:
        """Imprime de forma organizada los resultados"""
        print("-----------------")
        print(title)
        print("-----------------")
        for element in info:
            for key, value in element.items():
                if value:
                    print(f"{key}: {value}")


