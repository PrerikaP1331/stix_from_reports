import os
import json
import shutil
import requests
from typing import Optional


# ============================================================
# ===================== ATT&CK UPDATER =======================
# ============================================================

ATTACK_RAW_URL = (
    "https://raw.githubusercontent.com/mitre/cti/master/"
    "enterprise-attack/enterprise-attack.json"
)


class AttackDatasetUpdater:
    def __init__(self, local_path: str):
        self.local_path = local_path

    # -----------------------------
    # Local Version
    # -----------------------------
    def _get_local_version(self) -> Optional[str]:
        if not os.path.exists(self.local_path):
            return None

        with open(self.local_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return data.get("spec_version")

    # -----------------------------
    # Remote Fetch
    # -----------------------------
    def _get_remote_bundle(self) -> dict:
        response = requests.get(ATTACK_RAW_URL, timeout=60)
        response.raise_for_status()
        return response.json()

    # -----------------------------
    # Validation
    # -----------------------------
    def _validate_bundle(self, bundle: dict):
        if "objects" not in bundle:
            raise ValueError("Invalid ATT&CK STIX bundle: missing 'objects'")
        return True

    # -----------------------------
    # Update Logic
    # -----------------------------
    def update(self) -> bool:
        print("[*] Checking for ATT&CK updates...")

        remote_bundle = self._get_remote_bundle()
        self._validate_bundle(remote_bundle)

        remote_version = remote_bundle.get("spec_version")
        local_version = self._get_local_version()

        print(f"    Local version : {local_version}")
        print(f"    Remote version: {remote_version}")

        if local_version == remote_version:
            print("[✓] ATT&CK dataset is up to date.")
            return False

        print("[+] Updating ATT&CK dataset...")

        temp_path = self.local_path + ".tmp"

        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(remote_bundle, f)

        shutil.move(temp_path, self.local_path)

        print("[✓] ATT&CK update complete.")
        return True


