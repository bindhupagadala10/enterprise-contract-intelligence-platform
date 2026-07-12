import json
import traceback
from pathlib import Path

from app.services.parser.parser_service import ParserService
from app.services.dir.builder import DIRBuilder
from app.services.dir.serializer import DIRSerializer
from app.services.knowledge.enricher import KnowledgeEnricher
from app.services.chunking.semantic_chunker import SemanticChunker
from app.services.storage.chunk_repository import ChunkRepository

MANIFEST = Path("data/manifests/atticus_manifest.json")

DIR_OUTPUT = Path("data/processed/dir")
CHUNK_OUTPUT = Path("data/processed/chunks")

with open(MANIFEST, "r", encoding="utf-8") as f:
    manifest = json.load(f)

# Change 5: Temporarily limit the manifest
#manifest = manifest[:5]

parser = ParserService()
builder = DIRBuilder()
enricher = KnowledgeEnricher()
chunker = SemanticChunker()

total = len(manifest)

successful = 0
failed = 0

print("=" * 80)
print(f"Starting ingestion of {total} documents")
print("=" * 80)

for index, document in enumerate(manifest, start=1):
    try:
        # Change 2: Check for existing files to allow resuming
        dir_file = DIR_OUTPUT / f"{document['document_id']}.json"
        chunk_file = CHUNK_OUTPUT / f"{document['document_id']}.json"

        if dir_file.exists() and chunk_file.exists():
            print(f"[{index}/{total}] Already processed.")
            successful += 1
            continue

        pdf = (
            Path("data/raw/CUAD_v1")
            / document["relative_path"]
        )

        print(f"\n[{index}/{total}] {pdf.name}")

        # -------------------------------------------------
        # Parse
        # -------------------------------------------------
        doc = parser.parse_document(pdf)

        # -------------------------------------------------
        # Build DIR
        # -------------------------------------------------
        # Change 3: Updated builder signature
        dir_document = builder.build(
            docling_document=doc,
            manifest_entry=document,
        )

        # -------------------------------------------------
        # Enrich
        # -------------------------------------------------
        dir_document = enricher.enrich(dir_document)

        # -------------------------------------------------
        # Save DIR
        # -------------------------------------------------
        DIRSerializer.save(
            dir_document,
            DIR_OUTPUT / f"{document['document_id']}.json",
        )

        # -------------------------------------------------
        # Chunk
        # -------------------------------------------------
        chunks = chunker.chunk(dir_document)

        # -------------------------------------------------
        # Save Chunks
        # -------------------------------------------------
        ChunkRepository.save(
            chunks,
            CHUNK_OUTPUT / f"{document['document_id']}.json",
        )

        successful += 1

        # Change 4: Clearer read-out
        print(f"✓ Nodes  : {len(dir_document.nodes)}")
        print(f"✓ Chunks : {len(chunks)}")
        print(f"✓ Saved")

    except Exception as e:
        failed += 1
        print(f"✗ FAILED : {document.get('filename', 'unknown')}")
        traceback.print_exc()

print("\n")
print("=" * 80)
print("INGESTION COMPLETE")
print("=" * 80)
print(f"Successful : {successful}")
print(f"Failed     : {failed}")
print("=" * 80)