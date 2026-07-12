from pydantic import BaseModel, Field


class Chunk(BaseModel):

    chunk_id: str

    document_id: str

    chunk_index: int

    section_title: str | None = None

    text: str

    node_ids: list[str] = Field(default_factory=list)

    page_start: int

    page_end: int

    metadata: dict = Field(default_factory=dict)