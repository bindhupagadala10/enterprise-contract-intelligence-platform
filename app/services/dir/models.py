from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

class NodeType(str, Enum):
    DOCUMENT = "document"
    TITLE = "title"
    SECTION = "section"
    PARAGRAPH = "paragraph"
    LIST = "list"
    LIST_ITEM = "list_item"
    TABLE = "table"
    IMAGE = "image"
    HEADER = "header"
    FOOTER = "footer"
    UNKNOWN = "unknown"

@dataclass
class Provenance:
    page: int | None = None
    bbox: Optional[list] = None

@dataclass
class DIRNode:
    node_id: str
    parent_id: Optional[str]
    order: int
    node_type: NodeType
    text: str
    level: Optional[int]
    provenance: Provenance
    children: List[str] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)

@dataclass
class DIRDocument:
    document_id: str
    filename: str
    relative_path: str
    dataset: str
    collection: Optional[str]
    partition: Optional[str]
    category: Optional[str]
    parser: str
    parser_version: str
    page_count: int
    nodes: List[DIRNode]
    metadata: dict = field(default_factory=dict)