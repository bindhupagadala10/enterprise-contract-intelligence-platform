from pathlib import Path

from app.services.parser.docling_adapter import DoclingAdapter


class ParserService:

    def __init__(self):
        self.parser = DoclingAdapter()

    def parse_document(self, pdf_path: Path):
        """
        Parse a PDF and return the native Docling Document object.
        """

        document = self.parser.parse(pdf_path)

        return document