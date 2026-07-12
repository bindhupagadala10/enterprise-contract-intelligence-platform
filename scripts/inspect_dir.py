import json
from pathlib import Path

DIR = Path("data/processed/dir")

file = next(DIR.glob("*.json"))

with open(file, "r", encoding="utf-8") as f:
    document = json.load(f)

print("=" * 80)
print("FIRST 20 NODES")
print("=" * 80)

for node in document["nodes"][:20]:
    print("-" * 60)
    print("TYPE:", node["node_type"])
    print("TEXT:", node["text"][:80])
    print("LEVEL:", node["level"])
    print("PARENT:", node["metadata"]["parent"])
    print("SELF :", node["metadata"]["self_ref"])