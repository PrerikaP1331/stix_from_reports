# test_taxii.py
from app.knowledge.taxii_client import MitreTaxiiClient

client = MitreTaxiiClient()
objects = client.fetch_enterprise_attack()

print("Sample object types:")
types = set(obj["type"] for obj in objects)
print(types)
