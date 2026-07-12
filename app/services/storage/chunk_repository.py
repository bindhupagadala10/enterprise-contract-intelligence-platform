import json
from pathlib import Path


class ChunkRepository:

    @staticmethod
    def save(chunks, output_path):

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(
            output_path,
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(

                [c.model_dump() for c in chunks],

                f,

                indent=4,

                ensure_ascii=False,

            )