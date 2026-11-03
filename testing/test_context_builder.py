from app.storage.vector_storage import ChromaVectorStore
from app.retrieval.retriever import Retriever
from app.retrieval.context_builder import ContextBuilder


class DummyEmbeddingProvider:
    def embed_query(self, text: str):
        return [0.01] * 746


store = ChromaVectorStore(
    persist_directory="./chroma_test_data",
    collection_name="test_collection",
)

retriever = Retriever(
    vector_store=store,
    embedding_provider=DummyEmbeddingProvider(),
)

results = retriever.retrieve(
    query="What happens when an unauthorized transaction is reported?",
    top_k=3,
    source="pdf",
)

builder = ContextBuilder()
context = builder.build(results)

print("\nRetrieved chunks:", len(results))
print("\nGenerated context:\n")
print(context)