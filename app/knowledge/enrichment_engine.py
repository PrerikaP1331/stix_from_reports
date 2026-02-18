import json
from collections import defaultdict
from typing import Dict, List, Optional


class EnrichmentEngine:
    def __init__(self, attack_path: str):
        self.attack_path = attack_path

        self.objects_by_id: Dict[str, dict] = {}
        self.objects_by_external_id: Dict[str, dict] = {}
        self.objects_by_name: Dict[str, dict] = {}
        self.relationships = defaultdict(list)

        # FIRST: load dataset
        self._load_datasets()

        # SECOND: build core indexes
        self._build_indexes()

        # THIRD: now index groups/malware/tools
        self.groups = self._index_groups()
        self.malware = self._index_malware()
        self.tools = self._index_tools()
        self.techniques = self._index_techniques()

        # FOURTH: build alias maps
        self.group_alias_map = self._build_alias_map(self.groups)
        self.malware_alias_map = self._build_alias_map(self.malware)
        self.tool_alias_map = self._build_alias_map(self.tools)
        self.technique_alias_map = self._build_alias_map(self.techniques)


    # -------------------------------------------------
    # Load Bundles
    # -------------------------------------------------
    def _load_bundle(self, path: str) -> List[dict]:
        with open(path, "r", encoding="utf-8") as f:
            bundle = json.load(f)
        return bundle.get("objects", [])

    def _load_datasets(self):
        print("[*] Loading ATT&CK dataset...")

        attack_objects = self._load_bundle(self.attack_path)

        self.attack_objects = attack_objects
        self.all_objects = attack_objects

        print(f"[✓] Loaded {len(self.all_objects)} total objects")

        # Now that attack_objects exists, build technique index
        self._build_technique_index()
        

    # -------------------------------------------------
    # Index Building
    # -------------------------------------------------
    def _build_indexes(self):
        print("[*] Building indexes...")

        for obj in self.all_objects:
            obj_id = obj.get("id")
            obj_name = obj.get("name")

            if obj_id:
                self.objects_by_id[obj_id] = obj

            if obj_name:
                self.objects_by_name[obj_name.lower()] = obj

            # External ID indexing (T1059, ATLAS-123, etc.)
            external_refs = obj.get("external_references", [])
            for ref in external_refs:
                external_id = ref.get("external_id")
                if external_id:
                    self.objects_by_external_id[external_id] = obj

            # Relationship indexing
            if obj.get("type") == "relationship":
                source = obj.get("source_ref")
                target = obj.get("target_ref")

                if source and target:
                    self.relationships[source].append(obj)

        print("[✓] Indexing complete")

    def _build_technique_index(self):
        self.attack_techniques = {}

        for obj in self.attack_objects:
            if obj.get("type") != "attack-pattern":
                continue

            external_refs = obj.get("external_references", [])
            for ref in external_refs:
                if ref.get("source_name") == "mitre-attack" and ref.get("external_id", "").startswith("T"):
                    tid = ref["external_id"]
                    self.attack_techniques[tid] = obj

    def _index_groups(self):
        return [
            obj for obj in self.attack_objects
            if obj.get("type") == "intrusion-set"
        ]


    def _index_malware(self):
        return [
            obj for obj in self.attack_objects
            if obj.get("type") == "malware"
        ]


    def _index_tools(self):
        return [
            obj for obj in self.attack_objects
            if obj.get("type") == "tool"
        ]
    
    def _index_techniques(self):
        return [
            obj for obj in self.attack_objects
            if obj.get("type") == "attack-pattern"
        ]

    def _build_alias_map(self, objects):
        alias_map = {}

        for obj in objects:
            names = []

            # Primary name
            if obj.get("name"):
                names.append(obj["name"])

            # ATT&CK alias field
            if obj.get("x_mitre_aliases"):
                names.extend(obj["x_mitre_aliases"])

            # Some objects may use generic aliases
            if obj.get("aliases"):
                names.extend(obj["aliases"])

            for name in names:
                alias_map[name.lower()] = obj

        return alias_map

    # -------------------------------------------------
    # Lookup Methods
    # -------------------------------------------------
    def get_by_stix_id(self, stix_id: str) -> Optional[dict]:
        return self.objects_by_id.get(stix_id)

    def get_by_external_id(self, external_id: str) -> Optional[dict]:
        return self.objects_by_external_id.get(external_id)

    def get_by_name(self, name: str) -> Optional[dict]:
        return self.objects_by_name.get(name.lower())

    def get_related(self, stix_id: str) -> List[dict]:
        return self.relationships.get(stix_id, [])

    def get_technique(self, technique_id: str) -> Optional[dict]:
        return self.get_by_external_id(technique_id)
