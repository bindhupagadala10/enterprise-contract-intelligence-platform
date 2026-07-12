import json
from pathlib import Path

from app.services.parser.parser_service import ParserService

MANIFEST = Path("data/manifests/atticus_manifest.json")

with open(MANIFEST, "r", encoding="utf-8") as f:
    manifest = json.load(f)

document_info = manifest[0]

relative_path = Path(
    *document_info["relative_path"].replace("\\", "/").split("/")
)

pdf = Path("data/raw/CUAD_v1") / relative_path

print(pdf)
print(pdf.exists())

docling_document = ParserService().parse_document(pdf)

print("=" * 60)
print("Document Parsed Successfully")
print(f"Input : {pdf}")
print("=" * 60)

print(type(docling_document))