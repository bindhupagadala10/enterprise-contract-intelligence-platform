from uuid import uuid4
from pathlib import PureWindowsPath

from app.services.dir.models import (
    DIRDocument,
    DIRNode,
    NodeType,
    Provenance,
)


class DIRBuilder:

    def build(
        self,
        docling_document,
        manifest_entry,
    ):
        nodes = []
        order = 0

        for item, level in docling_document.iterate_items():
            text = ""
            if hasattr(item, "text"):
                text = item.text.strip()
            
            label = item.label.value.lower()
            node_type = self.map_type(label)
            page = None
            bbox = None
            
            if getattr(item, "prov", None):
                prov = item.prov[0]
                page = prov.page_no
                bbox = (
                    list(prov.bbox.as_tuple())
                    if prov.bbox is not None
                    else None
                )

            node = DIRNode(
                node_id=str(uuid4()),
                parent_id=None,
                order=order,
                node_type=node_type,
                text=text,
                level=level,
                provenance=Provenance(
                    page=page,
                    bbox=bbox,
                ),
                metadata={
                    "docling_type": item.__class__.__name__,
                    "label": label,
                },
            )
            nodes.append(node)
            order += 1

        parts = PureWindowsPath(manifest_entry["relative_path"]).parts
        collection = parts[0] if len(parts) > 0 else None
        partition = parts[1] if len(parts) > 1 else None
        category = parts[2] if len(parts) > 2 else None

        return DIRDocument(
            document_id=manifest_entry["document_id"],
            filename=manifest_entry["filename"],
            relative_path=manifest_entry["relative_path"],
            dataset="CUAD_v1",
            collection=collection,
            partition=partition,
            category=category,
            parser="docling",
            parser_version="1.0",
            page_count=docling_document.num_pages(),
            nodes=nodes,
        )

    def map_type(self, label):
        mapping = {
            "title": NodeType.TITLE,
            "section_header": NodeType.SECTION,
            "text": NodeType.PARAGRAPH,
            "list": NodeType.LIST,
            "list_item": NodeType.LIST_ITEM,
            "table": NodeType.TABLE,
            "picture": NodeType.IMAGE,
            "page_header": NodeType.HEADER,
            "page_footer": NodeType.FOOTER,
        }
        return mapping.get(
            label,
            NodeType.UNKNOWN,
        )