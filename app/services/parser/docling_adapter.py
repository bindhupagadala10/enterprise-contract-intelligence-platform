from pathlib import Path

from docling.document_converter import DocumentConverter


class DoclingAdapter:

    def __init__(self):

        self.converter = DocumentConverter()

    def parse(
        self,
        pdf_path: Path
    ):

        result = self.converter.convert(pdf_path)

        return result.document