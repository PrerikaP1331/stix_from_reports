from app.extraction.input_handler import InputHandler

# Test raw text
text = InputHandler.from_text("  Hello world attack report  ")
print(text)

# Test URL (replace with real article)
url_text = InputHandler.from_url("https://example.com")
print(url_text[:500])

# Test PDF (replace with real file)
pdf_text = InputHandler.from_pdf("sample.pdf")
print(pdf_text[:500])
