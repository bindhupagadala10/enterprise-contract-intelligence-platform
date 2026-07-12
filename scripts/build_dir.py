import json
from pathlib import Path
from app.services.knowledge.enricher import KnowledgeEnricher
from app.services.parser.parser_service import ParserService
from app.services.dir.builder import DIRBuilder
from app.services.dir.serializer import DIRSerializer

MANIFEST = Path("data/manifests/atticus_manifest.json")

with open(MANIFEST, "r", encoding="utf-8") as f:
    manifest = json.load(f)

doc_info = manifest[0]

pdf = Path("data/raw/CUAD_v1") / doc_info["relative_path"]

doc = ParserService().parse_document(pdf)

dir_document = DIRBuilder().build(

    docling_document=doc,

    document_id=doc_info["document_id"],

    filename=doc_info["filename"],

)

dir_document = KnowledgeEnricher().enrich(
    dir_document
)

output = Path(

    f"data/processed/dir/{doc_info['document_id']}.json"

)

DIRSerializer.save(

    dir_document,

    output,

)

print("=" * 70)
print("DIR BUILT SUCCESSFULLY")
print(f"Nodes : {len(dir_document.nodes)}")
print(f"Saved : {output}")
print("=" * 70)