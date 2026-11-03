from app.ingestion.pipeline import IngestionPipeline
from app.storage.vector_storage import ChromaVectorStore


pipeline = IngestionPipeline()
document, chunks = pipeline.ingest_pdf("sample_data/test.pdf")

embeddings = [
    [0.01] * 746
    for _ in chunks
]

store = ChromaVectorStore(
    persist_directory="./chroma_test_data",
    collection_name="test_collection",
)

store.add_chunks(chunks, embeddings)

print("Document:", document.title)
print("Stored chunks:", store.count())

query_embedding = [0.01] * 746
results = store.search(query_embedding, top_k=3)

for i, content in enumerate(results["documents"][0]):
    print(f"\nResult {i + 1}")
    print("Content:", content)
    print("Metadata:", results["metadatas"][0][i])
    print("Distance:", results["distances"][0][i])
re = ChromaVectorStore(
    persist_directory="./chroma_test_data",
    collection_name="test_collection",
)

store.add_chunks(chunks, embeddings)

print("Stored chunks:", store.count())

query_embedding = [0.01] * 746
results = store.search(query_embedding, top_k=3)

for i, content in enumerate(results["documents"][0]):
    print(f"\nResult {i + 1}")
    print("Content:", content)
    print("Metadata:", results["metadatas"][0][i])
    print("Distance:", results["distances"][0][i])