from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class TechniqueMatcher:

    def __init__(self, enrichment_engine):
        self.engine = enrichment_engine
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.technique_ids = []
        self.technique_embeddings = None

        self._prepare_embeddings()

    def _prepare_embeddings(self):
        descriptions = []

        for tid, obj in self.engine.attack_techniques.items():
            desc = obj.get("description", "")
            if desc:
                self.technique_ids.append(tid)
                descriptions.append(desc)

        self.technique_embeddings = self.model.encode(descriptions, convert_to_numpy=True)

    def match(self, text: str, top_n: int = 3):
        query_embedding = self.model.encode([text], convert_to_numpy=True)

        similarities = cosine_similarity(query_embedding, self.technique_embeddings)[0]

        top_indices = np.argsort(similarities)[::-1][:top_n]

        results = []
        for idx in top_indices:
            results.append({
                "technique_id": self.technique_ids[idx],
                "score": float(similarities[idx])
            })

        return results
