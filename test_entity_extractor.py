from app.knowledge.enrichment_engine import EnrichmentEngine
from app.nlp.entity_extractor import EntityExtractor
from app.knowledge.relationship_resolver import RelationshipResolver
from app.stix.stix_builder import STIXBuilder

def main():
    engine = EnrichmentEngine("app/data/attack-enterprise.json")

    extractor = EntityExtractor(engine)

    test_text = """ 
    APT29 used T1059.001 and phishing to deploy TrickBot.
    """

    # 1️⃣ Extract entities
    entities = extractor.extract_entities(test_text)

    print("\n===== ENTITY EXTRACTION TEST =====\n")

    for category, objects in entities.items():
        print(f"\n--- {category.upper()} ---")
        if not objects:
            print("None found")
        for obj in objects:
            print(f"Name: {obj.get('name')}")
            print(f"STIX ID: {obj.get('id')}")
            print("-" * 40)

    # 2️⃣ Infer relationships
    resolver = RelationshipResolver(engine)
    relationships = resolver.infer_relationships(entities)

    print("\n===== INFERRED RELATIONSHIPS =====\n")

    for rel in relationships:
        print(f"{rel['source']['name']} → {rel['relationship_type']} → {rel['target']['name']}")

    # 3️⃣ Build STIX bundle
    bundle = STIXBuilder.build_from_entities(entities, relationships)

    print("\n===== STIX BUNDLE OBJECT COUNT =====")
    print(len(bundle.objects))

    

if __name__ == "__main__":
    main()
