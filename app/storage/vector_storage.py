import chromadb
from app.ingestion.schemas import DocumentChunk


class ChromaVectorStore:
    def __init__(
        self,
        persist_directory="./chroma_data",
        collection_name="enterprise_knowledge",
        embedding_dimensions=746,
    ):
        self.embedding_dimensions = embedding_dimensions

        self.client = chromadb.PersistentClient(
            path=persist_directory
        )

        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    def add_chunks(self, chunks: list[DocumentChunk], embeddings: list[list[float]]):
        if not chunks:
            raise ValueError("No chunks provided")

        if len(chunks) != len(embeddings):
            raise ValueError("Chunks and embeddings count mismatch")

        if any(len(vector) != self.embedding_dimensions for vector in embeddings):
            raise ValueError(
                f"Each embedding must have {self.embedding_dimensions} dimensions"
            )

        self.collection.upsert(
            ids=[chunk.chunk_id for chunk in chunks],
            documents=[chunk.content for chunk in chunks],
            embeddings=embeddings,
            metadatas=[
                {
                    "document_id": chunk.document_id,
                    "chunk_index": chunk.chunk_index,
                    "page_number": chunk.page_number or 0,
                    **chunk.metadata,
                }
                for chunk in chunks
            ],
        )

    def search(
    self,
    query_embedding: list[float],
    top_k=5,
    filters: dict | None = None,
):
        if not query_embedding:
            raise ValueError("Query embedding cannot be empty")

        if len(query_embedding) != self.embedding_dimensions:
            raise ValueError(
                f"Query embedding must have {self.embedding_dimensions} dimensions"
            )

        if top_k <= 0:
            raise ValueError("top_k must be greater than zero")

        if self.collection.count() == 0:
            return {
                "ids": [[]],
                "documents": [[]],
                "metadatas": [[]],
                "distances": [[]],
            }

        query_args = {
            "query_embeddings": [query_embedding],
            "n_results": min(top_k, self.collection.count()),
            "include": ["documents", "metadatas", "distances"],
        }

        if filters:
            query_args["where"] = filters

        return self.collection.query(**query_args)


    def count(self):
        return self.collection.count()