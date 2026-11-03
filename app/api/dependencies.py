from app.core.config import settings
from app.embeddings.custom_provider import CustomEmbeddings
from app.storage.vector_storage import ChromaVectorStore
from app.retrieval.retriever import Retriever
from app.retrieval.context_builder import ContextBuilder
from app.services.llm_service import LLMService
from app.services.rag_services import RAGService


embedding_provider = CustomEmbeddings()

vector_store = ChromaVectorStore(
    persist_directory=settings.chroma_path,
    collection_name=settings.chroma_collection,
    embedding_dimensions=746,
)

retriever = Retriever(
    vector_store=vector_store,
    embedding_provider=embedding_provider,
)

context_builder = ContextBuilder()
llm_service = LLMService()

rag_service = RAGService(
    retriever=retriever,
    context_builder=context_builder,
    llm_service=llm_service,
)


def get_rag_service() -> RAGService:
    return rag_service