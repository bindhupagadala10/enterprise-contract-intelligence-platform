from pathlib import Path
import json
import uuid
from datetime import datetime

RAW_DATA = Path("data/raw/CUAD_v1")
MANIFEST_DIR = Path("data/manifests")
MANIFEST_DIR.mkdir(parents=True, exist_ok=True)

MANIFEST_PATH = MANIFEST_DIR / "atticus_manifest.json"


def discover_pdfs(root: Path):
    return sorted(root.rglob("*.pdf"))


def build_manifest(pdf_files):

    manifest = []

    for pdf in pdf_files:

        try:
            category = pdf.parent.name
        except Exception:
            category = "Unknown"

        manifest.append(
            {
                "document_id": str(uuid.uuid4()),
                "filename": pdf.name,
                "relative_path": str(
                    pdf.relative_to(RAW_DATA)
                ),
                "category": category,
                "parser": "docling",
                "status": "PENDING",
                "created_at": datetime.utcnow().isoformat(),
                "processing": {
                    "parsed": False,
                    "chunked": False,
                    "embedded": False,
                    "indexed": False,
                    "graph_built": False
                }
            }
        )

    return manifest


def save_manifest(manifest):

    with open(
        MANIFEST_PATH,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            manifest,
            f,
            indent=4
        )


def main():

    pdfs = discover_pdfs(RAW_DATA)

    manifest = build_manifest(pdfs)

    save_manifest(manifest)

    print("=" * 60)
    print(f"Discovered : {len(pdfs)} PDFs")
    print(f"Manifest   : {MANIFEST_PATH}")
    print("=" * 60)


if __name__ == "__main__":
    main()