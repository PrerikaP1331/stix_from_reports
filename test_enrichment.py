from app.knowledge.enrichment_engine import EnrichmentEngine

engine = EnrichmentEngine(
    "app/data/attack-enterprise.json"
)

technique = engine.get_technique("T1059")

if technique:
    print("Technique Name:", technique.get("name"))
    print("Description snippet:", technique.get("description")[:200])
else:
    print("Technique not found")
