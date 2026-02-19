import requests
from bs4 import BeautifulSoup
from pdfminer.high_level import extract_text
import tempfile


class InputHandler:

    @staticmethod
    def from_text(text: str) -> str:
        return text.strip()
    @staticmethod
    def from_url(url: str) -> str:
        import requests
        from bs4 import BeautifulSoup

        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        for script in soup(["script", "style"]):
            script.extract()

        return soup.get_text(separator=" ").strip()

    @staticmethod
    def from_pdf(uploaded_file) -> str:
        # Streamlit uploaded file
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name

        text = extract_text(tmp_path)
        return text.strip()