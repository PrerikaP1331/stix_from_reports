import requests
from bs4 import BeautifulSoup
from pdfminer.high_level import extract_text


class InputHandler:

    @staticmethod
    def from_text(text: str) -> str:
        return text.strip()

    @staticmethod
    def from_url(url: str) -> str:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove scripts and styles
        for script in soup(["script", "style"]):
            script.extract()

        text = soup.get_text(separator=" ")
        return text.strip()

    @staticmethod
    def from_pdf(pdf_path: str) -> str:
        text = extract_text(pdf_path)
        return text.strip()
