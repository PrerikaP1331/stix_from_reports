import json
import os
import requests
import tempfile
import shutil



class ThreatKnowledgeBase:

    ATTACK_URL = "https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json"
    ATLAS_URL = "https://raw.githubusercontent.com/mitre-atlas/atlas-data/main/atlas-data.json"

    def __init__(self, attack_path: str, atlas_path: str = None):
        self.attack_path = attack_path
        self.atlas_path = atlas_path

        self.attack_data = self._load_json(attack_path)
        self.atlas_data = self._load_json(atlas_path) if atlas_path else None

        # Indexed stores
        self.techniques = {}
        self.groups = {}
        self.software = {}

        self._index_attack()
        if self.atlas_data:
            self._index_atlas()

    def _load_json(self, path):
        if not path or not os.path.exists(path):
            raise FileNotFoundError(f"Dataset not found: {path}")
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _index_attack(self):
        for obj in self.attack_data.get("objects", []):
            if obj.get("type") == "attack-pattern":
                external_id = self._extract_external_id(obj)
                if external_id:
                    self.techniques[external_id] = obj

            elif obj.get("type") == "intrusion-set":
                self.groups[obj["name"].lower()] = obj

            elif obj.get("type") in ["malware", "tool"]:
                self.software[obj["name"].lower()] = obj

    def _index_atlas(self):
        for obj in self.atlas_data.get("objects", []):
            if obj.get("type") == "attack-pattern":
                external_id = self._extract_external_id(obj)
                if external_id:
                    self.techniques[external_id] = obj

    def _extract_external_id(self, obj):
        for ref in obj.get("external_references", []):
            if ref.get("external_id"):
                return ref["external_id"]
        return None

    # ----------------------
    # Public Lookup Methods
    # ----------------------

    def get_technique(self, technique_id: str):
        return self.techniques.get(technique_id)

    def search_group(self, name: str):
        return self.groups.get(name.lower())

    def search_software(self, name: str):
        return self.software.get(name.lower())

    def stats(self):
        return {
            "techniques": len(self.techniques),
            "groups": len(self.groups),
            "software": len(self.software)
        }
    def _extract_dataset_version(self, data):
        # Try to extract x_mitre_version
        for obj in data.get("objects", []):
            if obj.get("type") == "x-mitre-matrix":
                return obj.get("x_mitre_version")
        return None

    def _download_json(self, url):
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.json()

    def _safe_replace(self, path, new_data):
        with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as tmp:
            json.dump(new_data, tmp)
            tmp_path = tmp.name

        shutil.move(tmp_path, path)

    def update_datasets(self):

        print("Checking for ATT&CK updates...")

        remote_attack = self._download_json(self.ATTACK_URL)
        remote_version = self._extract_dataset_version(remote_attack)
        local_version = self._extract_dataset_version(self.attack_data)

        if remote_version and remote_version != local_version:
            print(f"New ATT&CK version found: {remote_version}")
            self._safe_replace(self.attack_path, remote_attack)
            self.attack_data = remote_attack
            self._reindex()
        else:
            print("ATT&CK dataset is up to date.")

        if self.atlas_data:
            print("Checking for ATLAS updates...")
            remote_atlas = self._download_json(self.ATLAS_URL)
            self._safe_replace(self.atlas_path, remote_atlas)
            self.atlas_data = remote_atlas
            self._reindex()

    def _reindex(self):
        self.techniques.clear()
        self.groups.clear()
        self.software.clear()
        self._index_attack()
        if self.atlas_data:
            self._index_atlas()
