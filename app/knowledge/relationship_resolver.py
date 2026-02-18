class RelationshipResolver:
    def __init__(self, knowledge_engine):
        self.engine = knowledge_engine

    def infer_relationships(self, entities):
        inferred = []

        # Flatten extracted entities
        extracted = []
        for category in entities.values():
            extracted.extend(category)

        extracted_ids = {obj["id"] for obj in extracted}

        # For each extracted entity
        for obj in extracted:
            obj_id = obj.get("id")

            related_relationships = self.engine.get_related(obj_id)

            for rel in related_relationships:
                if rel.get("relationship_type") == "uses":

                    target_id = rel.get("target_ref")
                    # Only keep relationships where target is also extracted
                    if target_id in extracted_ids:

                        target = self.engine.get_by_stix_id(target_id)

                        if target:
                            inferred.append({
                                "source": obj,
                                "target": target,
                                "relationship_type": "uses"
                            })

        return inferred
