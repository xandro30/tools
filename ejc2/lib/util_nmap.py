import nmap
import pandas as pd
from io import StringIO
import vulners


api_key = "4W6SEF0M1TGWEN6CE36RVHN2W5853Q37ED4NE4GRC6DGPSMK1E22LJHNGB5UYPAM" 


def get_cpe_info(list_cpe: list) -> list:
    """Recupera la información mediante cpe"""
    
    vulners_api = vulners.Vulners(api_key=api_key)
    info = []
    for cpe in list_cpe:
        cpe_results = vulners_api.cpeVulnerabilities(cpe)
        if any(cpe_results):
            cpe_exploit_list = cpe_results.get('exploit')
            cpe_vulnerabilities_list = [cpe_results.get(key) for key in cpe_results if key not in ['info', 'blog', 'bugbounty']]
            info.append(cpe_vulnerabilities_list)

    if any(info):
        print(info)
    return info


def get_software_vulnerabilities(df: pd.DataFrame) -> list:
    """Recupera la información mediante el producto y la versión"""
    vulners_api = vulners.Vulners(api_key=api_key)
    info = []

    for index, row in df.iterrows():
        results = vulners_api.softwareVulnerabilities(str(row.product), str(row.version))
        if any(results):
            exploit_list = results.get('exploit')
            vulnerabilities_list = [results.get(key) for key in results if key not in ['info', 'blog', 'bugbounty']]
            info.append(vulnerabilities_list)

    if any(info):
        print(info)
    return info


def basic_scan(dns_info: dict, whois_info: dict):
    """Lanza un scanneo basico de nmap"""
    nm = nmap.PortScanner()
    ips = "".join(dns_info['A'])
    hosts = f"{ips} {dns_info['domain']}"

    print("\n********************")
    print("Nmap:")
    print("********************\n")
    print("Lanzando scanner...\n")
    _ = nm.scan(hosts=hosts, arguments="-sV -n -A -T5")
    csv_data = nm.csv()
    df = pd.read_csv(StringIO(csv_data), sep=";")
    df = df.where(pd.notnull(df), None)

    print(df)
    try:
        cpe_info = get_cpe_info(df['cpe'].tolist())
        software_vulnerability = get_software_vulnerabilities(df[['product', 'version']])
    except:
        pass
    return df


