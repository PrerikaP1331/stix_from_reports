from typing import Dict, List
import re

class EntityExtractor:
    def __init__(self, knowledge_engine):
        self.engine = knowledge_engine

    def extract_entities(self, text: str) -> Dict[str, List[dict]]:
        text_lower = text.lower()

        # --- Name-based matching ---
        found_groups = self._match_entities(text_lower, self.engine.group_alias_map)
        found_malware = self._match_entities(text_lower, self.engine.malware_alias_map)
        found_tools = self._match_entities(text_lower, self.engine.tool_alias_map)
        found_techniques = self._match_entities(text_lower, self.engine.technique_alias_map)

        # -----------------------------------------
        # NEW: Detect technique IDs like T1059 or T1566.001
        # -----------------------------------------
        technique_ids = re.findall(r"\bT\d{4}(?:\.\d{3})?\b", text)

        resolved_techniques = []

        for tid in technique_ids:
            obj = self.engine.get_by_external_id(tid)
            if obj:
                resolved_techniques.append(obj)

        # -----------------------------------------
        # Merge name-based + ID-based techniques
        # -----------------------------------------
        all_techniques = {obj["id"]: obj for obj in found_techniques}

        for obj in resolved_techniques:
            all_techniques[obj["id"]] = obj

        found_techniques = list(all_techniques.values())

        return {
            "groups": found_groups,
            "malware": found_malware,
            "tools": found_tools,
            "techniques": found_techniques
        }


    def _match_entities(self, text: str, alias_map: dict):
        matched = []
        seen_ids = set()

        for alias, obj in alias_map.items():
            # Skip very short aliases (avoid false matches like "at")
            if len(alias) < 4:
                continue

            pattern = r"\b" + re.escape(alias) + r"\b"

            if re.search(pattern, text):
                obj_id = obj.get("id")
                if obj_id not in seen_ids:
                    matched.append(obj)
                    seen_ids.add(obj_id)

        return matched

