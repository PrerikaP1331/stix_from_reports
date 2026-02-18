from stix2 import (
    IPv4Address,
    DomainName,
    URL,
    File,
    Vulnerability,
    Indicator,
    Bundle, 
    Relationship
)
from datetime import datetime


class STIXBuilder:

    @staticmethod
    def build_from_iocs(iocs: dict) -> Bundle:
        objects = []
        relationships = []
        observable_objects = []

        # IPv4
        for ip in iocs.get("ips", []):
            obj = IPv4Address(value=ip)
            objects.append(obj)
            observable_objects.append(obj)

        # Domains
        for domain in iocs.get("domains", []):
            obj = DomainName(value=domain)
            objects.append(obj)
            observable_objects.append(obj)

        # URLs
        for url in iocs.get("urls", []):
            obj = URL(value=url.rstrip("."))
            objects.append(obj)
            observable_objects.append(obj)

        # File hashes
        for md5 in iocs.get("md5", []):
            obj = File(hashes={"MD5": md5})
            objects.append(obj)
            observable_objects.append(obj)

        for sha1 in iocs.get("sha1", []):
            obj = File(hashes={"SHA1": sha1})
            objects.append(obj)
            observable_objects.append(obj)

        for sha256 in iocs.get("sha256", []):
            obj = File(hashes={"SHA256": sha256})
            objects.append(obj)
            observable_objects.append(obj)

        # CVEs
        for cve in iocs.get("cves", []):
            vuln = Vulnerability(name=cve)
            objects.append(vuln)

            # relate vulnerability to all observables
            for obs in observable_objects:
                rel = Relationship(
                    relationship_type="related-to",
                    source_ref=vuln.id,
                    target_ref=obs.id
                )
                relationships.append(rel)

        return Bundle(objects + relationships)
    
    @staticmethod
    def build_from_entities(entities: dict, relationships: list) -> Bundle:
        objects = []
        relationship_objects = []

        added_ids = set()

        # Add extracted entities
        for category in entities.values():
            for obj in category:
                if obj["id"] not in added_ids:
                    objects.append(obj)
                    added_ids.add(obj["id"])

        # Add inferred relationships
        for rel in relationships:
            relationship_obj = Relationship(
                relationship_type=rel["relationship_type"],
                source_ref=rel["source"]["id"],
                target_ref=rel["target"]["id"]
            )
            relationship_objects.append(relationship_obj)

        return Bundle(objects + relationship_objects, allow_custom=True)
