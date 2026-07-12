from uuid import uuid4

from app.services.chunking.chunk_models import Chunk
from app.services.dir.models import NodeType


class SemanticChunker:
    MAX_WORDS = 350
    MAX_CHARS = 1800

    def chunk(self, document):
        chunks = []
        current_nodes = []
        current_text = []
        current_title = None
        current_page = 1
        chunk_index = 0

        for node in document.nodes:
            # Skip headers/footers
            if node.node_type in {
                NodeType.HEADER,
                NodeType.FOOTER,
            }:
                continue

            # New section starts a new chunk
            if node.node_type in {
                NodeType.TITLE,
                NodeType.SECTION,
            }:
                if current_text:
                    chunks.append(
                        self._build_chunk(
                            document,
                            chunk_index,
                            current_title,
                            current_nodes,
                            current_text,
                            current_page,
                        )
                    )
                    chunk_index += 1

                current_nodes = []
                current_text = []

                current_title = node.text
                current_page = node.provenance.page or 1

            current_nodes.append(node)

            if node.text.strip():
                current_text.append(node.text)

            # Check limits for mid-section splitting
            current_words = len(" ".join(current_text).split())
            current_chars = len("\n\n".join(current_text))

            if (
                current_nodes
                and (current_words >= self.MAX_WORDS or current_chars >= self.MAX_CHARS)
            ):
                chunks.append(
                    self._build_chunk(
                        document,
                        chunk_index,
                        current_title,
                        current_nodes,
                        current_text,
                        current_page,
                    )
                )
                chunk_index += 1
                current_nodes = []
                current_text = []
                current_page = node.provenance.page or current_page

        # Last chunk
        if current_text:
            chunks.append(
                self._build_chunk(
                    document,
                    chunk_index,
                    current_title,
                    current_nodes,
                    current_text,
                    current_page,
                )
            )

        return chunks

    def _build_chunk(
        self,
        document,
        chunk_index,
        title,
        nodes,
        text,
        page,
    ):
        return Chunk(
            chunk_id=str(uuid4()),
            document_id=document.document_id,
            chunk_index=chunk_index,
            section_title=title,
            text="\n\n".join(text),
            node_ids=[n.node_id for n in nodes],
            page_start=page,
            page_end=(
                nodes[-1].provenance.page
                if nodes and nodes[-1].provenance
                else page
            ),
            metadata={
                "dataset": document.dataset,
                "collection": document.collection,
                "partition": document.partition,
                "category": document.category,
                "filename": document.filename,
                "section_title": title,
                "num_nodes": len(nodes),
                "word_count": len(" ".join(text).split()),
                "char_count": len("\n\n".join(text)),
                "is_heading": False,
                "is_leaf": True,
                "chunk_candidate": True,
                "embedding_status": "pending"
            }
        )