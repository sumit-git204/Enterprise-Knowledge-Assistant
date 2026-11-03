from app.storage.vector_storage import ChromaVectorStore
from app.retrieval.retriever import Retriever
from app.retrieval.context_builder import ContextBuilder
from app.services.llm_service import LLMService
from app.services.rag_services import RAGService


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

rag = RAGService(
    retriever=retriever,
    context_builder=ContextBuilder(),
    llm_service=LLMService(),
)

result = rag.ask(
    question="What should the bank do when an unauthorized debit is reported?",
    top_k=3,
    source="pdf",
)

print("\nQuestion:")
print(result["question"])

print("\nAnswer:")
print(result["answer"])

print("\nSources:")
for source in result["sources"]:
    print(source)
from app.retrieval.retriever import Retriever
from app.retrieval.context_builder import ContextBuilder
from app.services.llm_service import LLMService


class RAGService:
    def __init__(
        self,
        retriever: Retriever,
        context_builder: ContextBuilder,
        llm_service: LLMService,
    ):
        self.retriever = retriever
        self.context_builder = context_builder
        self.llm_service = llm_service

    def ask(self, question: str, top_k: int = 5, source: str | None = None):
        retrieved_chunks = self.retriever.retrieve(
            query=question,
            top_k=top_k,
            source=source,
        )

        context = self.context_builder.build(retrieved_chunks)

        answer = self.llm_service.generate_answer(
            question=question,
            context=context,
        )

        return {
            "question": question,
            "answer": answer,
            "sources": [
                chunk["citation"] for chunk in retrieved_chunks
            ],
        }