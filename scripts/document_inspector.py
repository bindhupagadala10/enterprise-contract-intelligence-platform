import json
from pathlib import Path
from pprint import pprint

from app.services.parser.parser_service import ParserService

MANIFEST = Path("data/manifests/atticus_manifest.json")

with open(MANIFEST, "r", encoding="utf-8") as f:
    manifest = json.load(f)

doc_info = manifest[0]

pdf = Path("data/raw/CUAD_v1") / doc_info["relative_path"]

doc = ParserService().parse_document(pdf)

print("=" * 80)
print("DOCUMENT SUMMARY")
print("=" * 80)

print("Name:", doc.name)
print("Pages:", doc.num_pages)

print()

print("=" * 80)
print("BODY")
print("=" * 80)
pprint(doc.body)

print()

print("=" * 80)
print("TEXT OBJECTS")
print("=" * 80)
print("Count:", len(doc.texts))
if doc.texts:
    pprint(doc.texts[0])

print()

print("=" * 80)
print("TABLES")
print("=" * 80)
print("Count:", len(doc.tables))
if doc.tables:
    pprint(doc.tables[0])

print()

print("=" * 80)
print("PICTURES")
print("=" * 80)
print("Count:", len(doc.pictures))
if doc.pictures:
    pprint(doc.pictures[0])

print()

print("=" * 80)
print("GROUPS")
print("=" * 80)
print("Count:", len(doc.groups))
if doc.groups:
    pprint(doc.groups[0])