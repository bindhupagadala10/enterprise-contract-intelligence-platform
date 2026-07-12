import json
from dataclasses import asdict
from pathlib import Path

class DIRSerializer:
    @staticmethod
    def save(document, output_path: Path):
        data = asdict(document)

        def scan(obj, path="root"):
            # If the object itself is a callable, we've found it
            if callable(obj):
                print(f"⚠️ CALLABLE FOUND: {path} -> {obj}")
                return

            # If it's a dict, scan its values
            if isinstance(obj, dict):
                for k, v in obj.items():
                    scan(v, f"{path}.{k}")
            # If it's a list, scan its items
            elif isinstance(obj, list):
                for i, v in enumerate(obj):
                    scan(v, f"{path}[{i}]")

        scan(data)

        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False,
                default=str,  # This will convert the method to a string so the file saves
            )