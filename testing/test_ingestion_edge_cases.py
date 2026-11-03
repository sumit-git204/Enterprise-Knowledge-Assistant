from pathlib import Path

from app.ingestion.pipeline import IngestionPipeline
from app.ingestion.schemas import (
    DataSource,
    Document,
    DocumentChunk,
    DocumentType,
)
from app.ingestion.validator import validate_document, validate_chunks


pipeline = IngestionPipeline(chunk_size=25, chunk_overlap=5)


def test_missing_file():
    try:
        pipeline.ingest_pdf("sample_data/missing.pdf")
    except FileNotFoundError:
        print("Missing file test passed")
    else:
        raise AssertionError("Missing file should raise FileNotFoundError")


def test_unsupported_file():
    try:
        pipeline.ingest_pdf("sample_data/test.txt")
    except ValueError:
        print("Unsupported file test passed")
    else:
        raise AssertionError("Unsupported file should raise ValueError")


def test_empty_document():
    document = Document(
        document_id="doc-1",
        source=DataSource.PDF,
        title="Empty Document",
        content="",
        document_type=DocumentType.DOCUMENT,
        source_id="source-1",
        checksum="checksum-1",
    )

    try:
        validate_document(document)
    except ValueError:
        print("Empty document test passed")
    else:
        raise AssertionError("Empty document should fail validation")


def test_empty_chunks():
    document = Document(
        document_id="doc-1",
        source=DataSource.PDF,
        title="Test Document",
        content="Test content",
        document_type=DocumentType.DOCUMENT,
        source_id="source-1",
        checksum="checksum-1",
    )

    try:
        validate_chunks(document, [])
    except ValueError:
        print("Empty chunks test passed")
    else:
        raise AssertionError("Empty chunks should fail validation")


def test_wrong_document_id():
    document = Document(
        document_id="doc-1",
        source=DataSource.PDF,
        title="Test Document",
        content="Test content",
        document_type=DocumentType.DOCUMENT,
        source_id="source-1",
        checksum="checksum-1",
    )

    chunk = DocumentChunk(
        chunk_id="chunk-1",
        document_id="wrong-doc-id",
        content="Test content",
        chunk_index=0,
        page_number=1,
    )

    try:
        validate_chunks(document, [chunk])
    except ValueError:
        print("Wrong document ID test passed")
    else:
        raise AssertionError("Wrong document ID should fail validation")


if __name__ == "__main__":
    test_missing_file()
    test_unsupported_file()
    test_empty_document()
    test_empty_chunks()
    test_wrong_document_id()

    print("\nAll ingestion edge-case tests passed")
