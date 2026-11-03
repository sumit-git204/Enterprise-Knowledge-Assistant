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