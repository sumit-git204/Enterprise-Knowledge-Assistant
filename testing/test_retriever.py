from app.storage.vector_storage import ChromaVectorStore
from app.retrieval.retriever import Retriever


class DummyEmbeddingProvider:
    def embed_query(self, text: str):
        return [0.01] * 746


store = ChromaVectorStore(
    persist_directory="./chroma_test_data",
    collection_name="test_collection",
)

provider = DummyEmbeddingProvider()

retriever = Retriever(
    vector_store=store,
    embedding_provider=provider,
)

results = retriever.retrieve(
    query="What happens when an unauthorized transaction is reported?",
    top_k=3,
)

for i, result in enumerate(results, start=1):
    print(f"\nResult {i}")
    print("Content:", result["content"])
    print("Score:", result["score"])
    print("Citation:", result["citation"])