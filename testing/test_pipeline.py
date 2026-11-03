from app.ingestion.pipeline import IngestionPipeline


pipeline = IngestionPipeline(
    chunk_size=25,
    chunk_overlap=5,
)

document, chunks = pipeline.ingest_pdf("sample_data/test.pdf")

print("Ingestion pipeline completed successfully")
print(f"Document ID: {document.document_id}")
print(f"Title: {document.title}")
print(f"Source: {document.source.value}")
print(f"Checksum: {document.checksum}")
print(f"Total chunks: {len(chunks)}")

for chunk in chunks:
    print(f"\nChunk {chunk.chunk_index}")
    print(f"Chunk ID: {chunk.chunk_id}")
    print(f"Document ID: {chunk.document_id}")
    print(f"Page: {chunk.page_number}")
    print(f"Content: {chunk.content}")
    print(f"Metadata: {chunk.metadata}")