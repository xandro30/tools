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

    info = {'domain': domain}
    for qtype in ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA', 'CNAME']:
        answer = dns.resolver.resolve(domain,qtype, raise_on_no_answer=False)
        _list = []
        for rdata in answer:
            if qtype == "TXT":
                for txt_string in rdata.strings:
                    _list.append(txt_string.decode("utf-8"))
            elif qtype == "CNAME":
                _list.append(rdata.target.decode("utf-8"))
            elif qtype == "SOA":
                _list.append({'serial': rdata.serial, 'tech': rdata.rname,
                            'refresh': rdata.refresh, 'retry': rdata.retry,
                            'expire': rdata.expire, 'minimun': rdata.minimum,
                            'mname': rdata.mname})
            else:
                _list.append(str(rdata))
        if any(_list):
            info[qtype] = _list

    print("\n********************")
    print("DNS info:")
    print("********************\n")
    print_console_domain_info(info)
    
    return info


def extract_domain(url: str) -> str:
    """recibe url|ipv4|ipv6 valida y devuelve el dominio"""
    domain = whois.extract_domain(url)
    return domain


def get_whois(domain: str) -> dict:
    """Realiza una consulta de whois y devuelve una lista"""
    who = whois.whois(domain)
    if who['domain_name']:
        info = {
            'domain': who.domain,
            'text': who.text,
            'registrar': who.registrar,
            'whois_server': who.whois_server,
            'updated_date': who.updated_date[-1].strftime("%Y/%m/%d %H:%M:%S") if isinstance(who.updated_date, list) else who.updated_date.strftime("%Y/%m/%d %H:%M:%S"),
            'creation_date': who.creation_date[-1].strftime("%Y/%m/%d %H:%M:%S")if isinstance(who.creation_date, list) else who.creation_date.strftime("%Y/%m/%d %H:%M:%S"),
            'expiration_date': who.expiration_date[-1].strftime("%Y/%m/%d %H:%M:%S") if isinstance(who.expiration_date, list) else who.expiration_date.strftime("%Y/%m/%d %H:%M:%S"),
            'name_servers': who.name_servers,
            'emails': who.emails,
            'name': who.name,
            'org': who.org,
            'address': who.address,
            'city': who.city,
            'zipcode': who.zipcode,
            'country': who.country
        }
    else:
        info = f"{domain}: {who.text}"
    
    print("\n********************")
    print("Whois info:")
    print("********************\n")
    print_console_domain_info(info)

    return info
