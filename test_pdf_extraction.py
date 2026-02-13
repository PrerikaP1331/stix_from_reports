from app.extraction.pdf_extractor import extract_text_from_pdf

doc = extract_text_from_pdf("sample.pdf")

print("\n=== METADATA ===")
print(doc.metadata)

print("\n=== PAGE COUNT ===")
print(len(doc.pages))

if doc.pages:
    print("\n=== FIRST PAGE PREVIEW ===")
    print(doc.pages[0].text[:500])