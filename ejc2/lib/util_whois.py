import dns.resolver
import whois



def print_console_domain_info(info: [dict, str], title: str = ""):
    """Función recursiva que imprime la información obtenida"""

    if isinstance(info, dict):
        for key, value in info.items():
            if isinstance(value, list) or isinstance(value, dict):
                print_console_domain_info(value, key)  #
            elif value is not None and len(value) < 100:
                print(f"tipo: {key} -> {value}")
    elif isinstance(info, list):
        print(f"tipo: {title}")
        for value in info:
            print(f"\t * {value}")
    else:
        print(f"tipo: {title}, {info}")


def get_dns_domain_info(domain: str) -> dict:
    """Realiza las consultas dns para obtener información"""
    a = dns.resolver.resolve(domain, 'A')
    mx = dns.resolver.resolve(domain, 'MX')
    ns = dns.resolver.resolve(domain, 'NS')
    aaaa = dns.resolver.resolve(domain, 'aaaa')

    info = {
        'a': {'canonical_name': a.canonical_name, 'name_server': a.nameserver, 'lines': a.rrset},
        'mx': {'canonical_name': mx.canonical_name, 'name_server': mx.nameserver, 'lines': mx.rrset},
        'ns': {'canonical_name': ns.canonical_name, 'name_server': mx.nameserver, 'lines': mx.rrset},
        'aaaa': {'canonical_name': aaaa.canonical_name, 'name_server': aaaa.nameserver, 'lines': aaaa.rrset},
    }
    print_console_domain_info(info)
    return info


def extract_domain(url: str) -> str:
    """recibe url|ipv4|ipv6 valida y devuelve el dominio"""
    domain = whois.extract_domain(url)
    return domain


def get_whois(domain: str) -> dict:
    """Realiza una consulta de whois y devuelve una lista"""
    who = whois.whois(domain)
    info = {
        'domain': who.domain,
        'text': who.text,
        'registrar': who.registrar,
        'whois_server': who.whois_server,
        'updated_date': who.updated_date[-1].strftime("%Y/%m/%d %H:%M:%S"),
        'creation_date': who.creation_date[-1].strftime("%Y/%m/%d %H:%M:%S"),
        'expiration_date': who.expiration_date[-1].strftime("%Y/%m/%d %H:%M:%S"),
        'name_servers': who.name_servers,
        'emails': who.emails,
        'name': who.name,
        'org': who.org,
        'address': who.address,
        'city': who.city,
        'zipcode': who.zipcode,
        'country': who.country
    }
    
    print_console_domain_info(info)

    return info
