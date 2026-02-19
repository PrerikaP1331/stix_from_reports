from stix2 import (
    IPv4Address,
    DomainName,
    URL,
    File,
    Vulnerability,
    Indicator,
    Relationship,
    Bundle
)
from datetime import datetime
from typing import List


class STIXBuilder:

    @staticmethod
    def build_full_bundle(entities: dict,
                          relationships: list,
                          iocs: List) -> Bundle:

        stix_objects = []
        relationship_objects = []
        added_ids = set()

        # =====================================================
        # 1️⃣ ADD ATT&CK ENTITIES
        # =====================================================
        for category in entities.values():
            for obj in category:
                if obj["id"] not in added_ids:
                    stix_objects.append(obj)
                    added_ids.add(obj["id"])

        # =====================================================
        # 2️⃣ ADD INFERRED RELATIONSHIPS (uses)
        # =====================================================
        for rel in relationships:
            relationship_obj = Relationship(
                relationship_type=rel["relationship_type"],
                source_ref=rel["source"]["id"],
                target_ref=rel["target"]["id"]
            )
            relationship_objects.append(relationship_obj)

        # =====================================================
        # 3️⃣ ADD IOCs AS INDICATORS
        # =====================================================
        for ioc in iocs:

            pattern = STIXBuilder._build_pattern(ioc)

            if not pattern:
                continue

            indicator = Indicator(
                name=f"{ioc.type} indicator",
                pattern=pattern,
                pattern_type="stix",
                description=ioc.context if ioc.context else None,
                valid_from=datetime.utcnow()
            )

            stix_objects.append(indicator)

        # =====================================================
        # 4️⃣ ADD CVEs AS Vulnerability objects
        # =====================================================
        for ioc in iocs:
            if ioc.type == "cve":
                vuln = Vulnerability(name=ioc.value)
                stix_objects.append(vuln)

        return Bundle(stix_objects + relationship_objects, allow_custom=True)

    # ---------------------------------------------------------
    # Pattern Builder
    # ---------------------------------------------------------
    @staticmethod
    def _build_pattern(ioc):

        if ioc.type == "ipv4":
            return f"[ipv4-addr:value = '{ioc.value}']"

        if ioc.type == "domain":
            return f"[domain-name:value = '{ioc.value}']"

        if ioc.type == "url":
            return f"[url:value = '{ioc.value}']"

        if ioc.type == "md5":
            return f"[file:hashes.MD5 = '{ioc.value}']"

        if ioc.type == "sha1":
            return f"[file:hashes.SHA1 = '{ioc.value}']"

        if ioc.type == "sha256":
            return f"[file:hashes.SHA256 = '{ioc.value}']"

        return None
