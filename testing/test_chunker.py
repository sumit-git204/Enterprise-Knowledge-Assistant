from pathlib import Path

from app.connectors.pdf_connector import PDFConnector
from app.ingestion.chunker import RecursiveChunker
from app.ingestion.normalizer import normalize_pdf

file_path = Path("sample_data/test.pdf")
extracted = PDFConnector().extract(file_path)
document = normalize_pdf(extracted, file_path)

chunker = RecursiveChunker(chunk_size=25, chunk_overlap=5)
chunks = chunker.chunk_document(document)

for chunk in chunks:
    print(f"\nChunk {chunk.chunk_index}")
    print(f"Page: {chunk.page_number}")
    print(chunk.content)
    print(f"Tokens: {len(chunker.tokenizer.encode(chunk.content))}")