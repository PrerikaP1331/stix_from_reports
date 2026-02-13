import fitz  # PyMuPDF
from typing import Dict
from app.extraction.document_model import Document, Page
from app.utils.logger import get_logger

logger = get_logger(__name__)


class PDFExtractionError(Exception):
    pass


def extract_pdf_metadata(doc: fitz.Document) -> Dict:
    metadata = doc.metadata or {}
    return {
        "title": metadata.get("title"),
        "author": metadata.get("author"),
        "creation_date": metadata.get("creationDate"),
        "producer": metadata.get("producer"),
    }


def extract_text_from_pdf(file_path: str) -> Document:
    try:
        doc = fitz.open(file_path)
    except Exception as e:
        logger.error(f"Failed to open PDF: {e}")
        raise PDFExtractionError("Invalid or corrupted PDF.")

    document = Document(
        filename=file_path.split("/")[-1],
        metadata=extract_pdf_metadata(doc)
    )

    for page_number in range(len(doc)):
        page = doc[page_number]
        text = page.get_text("text")

        if text:
            document.pages.append(
                Page(
                    number=page_number + 1,
                    text=text.strip()
                )
            )

    doc.close()

    logger.info(f"Extracted {len(document.pages)} pages from PDF.")

    return document
