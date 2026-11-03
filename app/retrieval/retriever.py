from app.storage.vector_storage import ChromaVectorStore


class Retriever:
    def __init__(self, vector_store: ChromaVectorStore, embedding_provider):
        self.vector_store = vector_store
        self.embedding_provider = embedding_provider

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        source: str | None = None,
    ):
        query = query.strip()

        if not query:
            raise ValueError("Query cannot be empty")

        if top_k <= 0:
            raise ValueError("top_k must be greater than zero")

        query_embedding = self.embedding_provider.embed_query(query)

        filters = None

        if source:
            filters = {"source": {"$eq": source.lower()}}

        results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
            filters=filters,
        )

        retrieved_chunks = []

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]
        ids = results.get("ids", [[]])[0]

        for i, content in enumerate(documents):
            metadata = metadatas[i] or {}

            retrieved_chunks.append(
                {
                    "chunk_id": ids[i],
                    "content": content,
                    "score": distances[i],
                    "citation": {
                        "source": metadata.get("source"),
                        "title": metadata.get("title"),
                        "source_id": metadata.get("source_id"),
                        "page_number": metadata.get("page_number"),
                        "document_id": metadata.get("document_id"),
                    },
                    "metadata": metadata,
                }
            )

        return retrieved_chunks