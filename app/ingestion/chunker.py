import re
from uuid import uuid4

import tiktoken

from app.ingestion.schemas import Document, DocumentChunk


class RecursiveChunker:
    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 75,
        encoding_name: str = "cl100k_base",
    ):
        if chunk_size <= 0:
            raise ValueError("chunk_size must be greater than 0")
        if chunk_overlap < 0 or chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap must be between 0 and chunk_size")

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.tokenizer = tiktoken.get_encoding(encoding_name)

    def _split_text(self, text: str) -> list[str]:
        separators = ["\n\n", "\n", r"(?<=[.!?])\s+", " "]

        for separator in separators:
            if separator.startswith("(?"):
                parts = re.split(separator, text)
            else:
                parts = text.split(separator)

            parts = [part.strip() for part in parts if part.strip()]

            if len(parts) > 1 and all(
                len(self.tokenizer.encode(part)) <= self.chunk_size
                for part in parts
            ):
                return parts

        tokens = self.tokenizer.encode(text)
        return [
            self.tokenizer.decode(tokens[i : i + self.chunk_size])
            for i in range(0, len(tokens), self.chunk_size - self.chunk_overlap)
        ]

    def chunk_document(self, document: Document) -> list[DocumentChunk]:
        chunks = []
        current_text = ""
        chunk_index = 0

        for piece in self._split_text(document.content):
            candidate = f"{current_text} {piece}".strip()
            candidate_tokens = self.tokenizer.encode(candidate)

            if len(candidate_tokens) <= self.chunk_size:
                current_text = candidate
                continue

            if current_text:
                chunks.append(
                    DocumentChunk(
                        chunk_id=str(uuid4()),
                        document_id=document.document_id,
                        content=current_text,
                        chunk_index=chunk_index,
                        page_number=1,
                        metadata={
                            "source": document.source.value,
                            "title": document.title,
                            "source_id": document.source_id,
                            "checksum": document.checksum,
                            "document_type": document.document_type.value,
                        }
                    )
                )

                chunk_index += 1

                current_tokens = self.tokenizer.encode(current_text)
                overlap_tokens = (
                    current_tokens[-self.chunk_overlap :]
                    if self.chunk_overlap
                    else []
                )
                current_text = self.tokenizer.decode(overlap_tokens).strip()

            current_text = f"{current_text} {piece}".strip()

        if current_text:
            chunks.append(
                DocumentChunk(
                    chunk_id=str(uuid4()),
                    document_id=document.document_id,
                    content=current_text,
                    chunk_index=chunk_index,
                    page_number=1,
                    metadata={
                        "source": document.source.value,
                        "title": document.title,
                        "source_id": document.source_id,
                        "checksum": document.checksum,
                        "document_type": document.document_type.value,
                    },
                )
            )

        return chunks