from app.ingestion.schemas import Document, DocumentChunk


def validate_document(document: Document) -> None:
    if not document.document_id.strip():
        raise ValueError("Document ID cannot be empty")

    if not document.title.strip():
        raise ValueError("Document title cannot be empty")

    if not document.content.strip():
        raise ValueError("Document content cannot be empty")

    if not document.source_id or not document.source_id.strip():
        raise ValueError("Document source ID is required")

    if not document.checksum or not document.checksum.strip():
        raise ValueError("Document checksum is required")


def validate_chunks(
    document: Document,
    chunks: list[DocumentChunk],
) -> None:
    if not chunks:
        raise ValueError("Document must contain at least one chunk")

    seen_indexes = set()

    for chunk in chunks:
        if not chunk.chunk_id.strip():
            raise ValueError("Chunk ID cannot be empty")

        if not chunk.content.strip():
            raise ValueError("Chunk content cannot be empty")

        if chunk.document_id != document.document_id:
            raise ValueError("Chunk document ID does not match")

        if chunk.chunk_index in seen_indexes:
            raise ValueError(f"Duplicate chunk index detected: {chunk.chunk_index}")

        if chunk.chunk_index < 0 or chunk.chunk_index >= len(chunks):
            raise ValueError(
                f"Chunk index {chunk.chunk_index} is out of expected sequential range [0, {len(chunks) - 1}]"
            )

        seen_indexes.add(chunk.chunk_index)