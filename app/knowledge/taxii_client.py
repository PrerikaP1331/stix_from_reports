from taxii2client.v21 import Server
from typing import List, Dict


MITRE_TAXII_URL = "https://cti-taxii.mitre.org/taxii/"


class MitreTaxiiClient:
    def __init__(self):
        self.server = Server(MITRE_TAXII_URL)
        self.api_root = self.server.api_roots[0]

    def _get_collection_by_title(self, title: str):
        for collection in self.api_root.collections:
            if collection.title == title:
                return collection
        raise ValueError(f"Collection '{title}' not found on MITRE TAXII server.")

    def fetch_enterprise_attack(self) -> List[Dict]:
        """
        Fetch full Enterprise ATT&CK STIX 2.1 collection.
        Returns list of STIX objects.
        """
        collection = self._get_collection_by_title("Enterprise ATT&CK")

        print(f"[+] Fetching collection: {collection.title}")
        bundle = collection.get_objects()

        objects = bundle.get("objects", [])
        print(f"[+] Retrieved {len(objects)} STIX objects")

        return objects
