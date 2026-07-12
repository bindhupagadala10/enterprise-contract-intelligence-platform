from app.services.dir.models import (
    DIRDocument,
    NodeType,
)


class KnowledgeEnricher:

    def enrich(
        self,
        document: DIRDocument,
    ) -> DIRDocument:

        for node in document.nodes:

            node.metadata.update({

                "word_count": self._word_count(node.text),

                "char_count": self._char_count(node.text),

                "is_heading": self._is_heading(node.node_type),

                "is_leaf": self._is_leaf(node),

                "chunk_candidate": self._is_chunk_candidate(node),

                "embedding_status": "pending",

            })

        return document

    def _word_count(
        self,
        text: str,
    ) -> int:

        if not text:
            return 0

        return len(text.split())

    def _char_count(
        self,
        text: str,
    ) -> int:

        return len(text)

    def _is_heading(
        self,
        node_type: NodeType,
    ) -> bool:

        return node_type in {

            NodeType.TITLE,

            NodeType.SECTION,

        }

    def _is_leaf(
        self,
        node,
    ) -> bool:

        return len(node.children) == 0

    def _is_chunk_candidate(
        self,
        node,
    ) -> bool:

        if node.node_type in {

            NodeType.HEADER,

            NodeType.FOOTER,

        }:

            return False

        if len(node.text.strip()) < 10:

            return False

        return True