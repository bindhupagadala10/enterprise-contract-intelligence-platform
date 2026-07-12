import json

with open(
    "data/manifests/atticus_manifest.json",
    "r",
    encoding="utf-8",
) as f:

    manifest = json.load(f)

print(manifest[0]["relative_path"])