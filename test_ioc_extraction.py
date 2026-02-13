from app.extraction.pdf_extractor import extract_text_from_pdf
from app.ioc.ioc_extractor import extract_iocs_from_document

doc = extract_text_from_pdf("sample.pdf")

iocs = extract_iocs_from_document(doc)

print("\n=== EXTRACTED IOCs ===")

for ioc in iocs:
    print(f"\nType: {ioc.type}")
    print(f"Value: {ioc.value}")
    print(f"Source: {ioc.source}")
    print(f"Context: {ioc.context}")
