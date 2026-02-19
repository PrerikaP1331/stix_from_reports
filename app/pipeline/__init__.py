# Initialize pipeline package
def __init__(self, attack_path="app/data/attack-enterprise.json"):
    self.engine = EnrichmentEngine(attack_path)
    self.entity_extractor = EntityExtractor(self.engine)
    self.relationship_resolver = RelationshipResolver(self.engine)
    self.technique_matcher = TechniqueMatcher(self.engine)
