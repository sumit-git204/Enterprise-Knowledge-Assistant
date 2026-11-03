from pathlib import Path

from app.connectors.pdf_connector import PDFConnector
from app.ingestion.chunker import RecursiveChunker
from app.ingestion.normalizer import normalize_pdf
from app.ingestion.schemas import Document, DocumentChunk
from app.ingestion.validator import validate_document, validate_chunks


class IngestionPipeline:
    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 75,
    ):
        self.connector = PDFConnector()
        self.chunker = RecursiveChunker(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    def ingest_pdf(
        self,
        file_path: str | Path,
    ) -> tuple[Document, list[DocumentChunk]]:
        file_path = Path(file_path)

        extracted = self.connector.extract(file_path)
        document = normalize_pdf(extracted, file_path)

        validate_document(document)

        chunks = self.chunker.chunk_document(document)

        validate_chunks(document, chunks)

        return document, chunks
