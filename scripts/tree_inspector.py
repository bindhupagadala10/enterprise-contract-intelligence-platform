from pathlib import Path
import json

from app.services.parser.parser_service import ParserService

MANIFEST = Path("data/manifests/atticus_manifest.json")

with open(MANIFEST, "r", encoding="utf-8") as f:
    manifest = json.load(f)

doc_info = manifest[0]
pdf = Path("data/raw/CUAD_v1") / doc_info["relative_path"]

doc = ParserService().parse_document(pdf)

print("=" * 80)
print("DOCUMENT TREE")
print("=" * 80)

doc.print_element_tree()