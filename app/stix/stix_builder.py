from stix2 import Indicator, IPv4Address, DomainName, Vulnerability, Bundle
from datetime import datetime

def create_indicator_for_ip(ip_value: str):
    ip_obj = IPv4Address(value=ip_value)

    indicator = Indicator(
        name=f"Malicious IP {ip_value}",
        pattern=f"[ipv4-addr:value = '{ip_value}']",
        pattern_type="stix",
        valid_from=datetime.utcnow()
    )

    return ip_obj, indicator


def create_indicator_for_domain(domain_value: str):
    domain_obj = DomainName(value=domain_value)

    indicator = Indicator(
        name=f"Malicious Domain {domain_value}",
        pattern=f"[domain-name:value = '{domain_value}']",
        pattern_type="stix",
        valid_from=datetime.utcnow()
    )

    return domain_obj, indicator


def create_vulnerability(cve_id: str):
    return Vulnerability(
        name=cve_id
    )


def create_bundle(objects):
    return Bundle(objects)
