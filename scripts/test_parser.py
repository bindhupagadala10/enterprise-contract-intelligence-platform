import json
from pathlib import Path

from app.services.parser.parser_service import ParserService

MANIFEST = Path("data/manifests/atticus_manifest.json")

with open(MANIFEST, "r", encoding="utf-8") as f:
    manifest = json.load(f)

document_info = manifest[0]

# Now using the Linux-native paths directly from the newly generated manifest
pdf = Path("data/raw/CUAD_v1") / document_info["relative_path"]

docling_document = ParserService().parse_document(pdf)

print("=" * 60)
print("Document Parsed Successfully")
print(f"Input : {pdf}")
print("=" * 60)

print(type(docling_document))