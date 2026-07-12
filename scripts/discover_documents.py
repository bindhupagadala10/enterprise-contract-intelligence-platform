from pathlib import Path

RAW_DATA = Path("data/raw/CUAD_v1")


def discover_pdfs(root: Path):
    return sorted(root.rglob("*.pdf"))


def main():
    pdfs = discover_pdfs(RAW_DATA)

    print("=" * 60)
    print(f"Found {len(pdfs)} PDF files\n")

    for pdf in pdfs[:10]:
        print(pdf)

    if len(pdfs) > 10:
        print("\n...")

main()