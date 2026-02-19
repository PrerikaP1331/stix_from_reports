import asyncio
from app.extraction.input_handler import InputHandler
from app.extraction.text_cleaner import normalize_whitespace
from app.ioc.ioc_extractor import extract_iocs_from_text
from app.ioc.ioc_models import IOC
from app.nlp.entity_extractor import EntityExtractor
from app.knowledge.enrichment_engine import EnrichmentEngine
from app.knowledge.relationship_resolver import RelationshipResolver
from app.enrichment.enrichment_orchestrator import enrich_all
from app.stix.stix_builder import STIXBuilder
from app.knowledge.technique_matcher import TechniqueMatcher


class CTIPipeline:

    def __init__(self, attack_path="app/data/attack-enterprise.json"):
        self.engine = EnrichmentEngine(attack_path)
        self.entity_extractor = EntityExtractor(self.engine)
        self.relationship_resolver = RelationshipResolver(self.engine)
        self.technique_matcher = TechniqueMatcher(self.engine)

    def process(self, source, input_type="text"):

        # 1️⃣ Extract raw text
        text = self._extract_text(source, input_type)

        text = normalize_whitespace(text)

        # 2️⃣ Extract IOCs (string-based fallback)
        iocs = extract_iocs_from_text(text)

        # 3️⃣ Enrich IOCs (async safe for Streamlit)
        try:
            iocs = asyncio.run(enrich_all(iocs))
        except RuntimeError:
            loop = asyncio.get_event_loop()
            iocs = loop.run_until_complete(enrich_all(iocs))


        # 4️⃣ Extract ATT&CK entities
        entities = self.entity_extractor.extract_entities(text)

        # 🔍 Semantic technique matching
        semantic_matches = self.technique_matcher.match(text, top_n=2)

        for match in semantic_matches:
            if match["score"] < 0.6:
                continue
            else:
                obj = self.engine.get_by_external_id(match["technique_id"])
                if obj:
                    # Avoid duplicates
                    if obj["id"] not in [t["id"] for t in entities["techniques"]]:
                        entities["techniques"].append(obj)

        # 5️⃣ Infer relationships
        relationships = self.relationship_resolver.infer_relationships(entities)

        # 6️⃣ Build STIX 2.1 bundle
        bundle = STIXBuilder.build_full_bundle(
            entities=entities,
            relationships=relationships,
            iocs=iocs
        )

        return bundle

    def _extract_text(self, source, input_type):

        if input_type == "text":
            return InputHandler.from_text(source)

        elif input_type == "pdf":
            return InputHandler.from_pdf(source)

        elif input_type == "url":
            return InputHandler.from_url(source)

        else:
            raise ValueError("Unsupported input type")

