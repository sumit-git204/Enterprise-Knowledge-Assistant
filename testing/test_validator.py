from pathlib import Path

from app.connectors.pdf_connector import PDFConnector
from app.ingestion.chunker import RecursiveChunker
from app.ingestion.normalizer import normalize_pdf
from app.ingestion.validator import validate_chunks, validate_document

file_path = Path("sample_data/test.pdf")

extracted = PDFConnector().extract(file_path)
document = normalize_pdf(extracted, file_path)

chunker = RecursiveChunker(chunk_size=25, chunk_overlap=5)
chunks = chunker.chunk_document(document)

validate_document(document)
validate_chunks(document, chunks)

print("Document validation passed")
print("Chunk validation passed")
print(f"Validated {len(chunks)} chunks")