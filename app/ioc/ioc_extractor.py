import re
from typing import List
from app.ioc.regex_patterns import *
from app.ioc.ioc_models import IOC
from app.extraction.document_model import Document


def extract_sentences(text: str):
    # First split by newline
    lines = text.split("\n")

    cleaned = []
    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Further split by sentence-ending punctuation (but preserve dots in IPs)
        parts = re.split(r'(?<=[!?])\s+', line)
        for part in parts:
            if part.strip():
                cleaned.append(part.strip())

    return cleaned

def find_context(value: str, sentences: List[str]) -> str:
    for sentence in sentences:
        if value in sentence:
            return sentence.strip()
    return None


def deduplicate_iocs(iocs: List[IOC]) -> List[IOC]:
    seen = set()
    unique = []

    for ioc in iocs:
        key = (ioc.type, ioc.value)
        if key not in seen:
            seen.add(key)
            unique.append(ioc)

    return unique


def extract_iocs_from_document(document: Document) -> List[IOC]:
    all_iocs = []

    patterns = [
        ("ipv4", IP_PATTERN),
        ("domain", DOMAIN_PATTERN),
        ("url", URL_PATTERN),
        ("md5", MD5_PATTERN),
        ("sha1", SHA1_PATTERN),
        ("sha256", SHA256_PATTERN),
        ("cve", CVE_PATTERN),
    ]

    for page in document.pages:
        sentences = extract_sentences(page.text)

        for ioc_type, pattern in patterns:
            matches = re.findall(pattern, page.text)

            for match in matches:
                context = find_context(match, sentences)

                ioc = IOC(
                    type=ioc_type,
                    value=match,
                    context=context,
                    source=f"Page {page.number}"
                )

                all_iocs.append(ioc)

    return deduplicate_iocs(all_iocs)
