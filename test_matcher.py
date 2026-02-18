from app.knowledge.enrichment_engine import EnrichmentEngine
from app.knowledge.technique_matcher import TechniqueMatcher

engine = EnrichmentEngine("app/data/attack-enterprise.json")
matcher = TechniqueMatcher(engine)

sample_text = """
The attacker executed PowerShell scripts to maintain persistence and execute commands remotely.
"""

results = matcher.match(sample_text)

for r in results:
    print(r)
