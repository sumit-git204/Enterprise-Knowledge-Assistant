class ContextBuilder:
    def build(self, retrieved_chunks: list[dict]) -> str:
        if not retrieved_chunks:
            return "No relevant information was found."

        context_parts = []

        for index, chunk in enumerate(retrieved_chunks, start=1):
            citation = chunk.get("citation", {})

            source = citation.get("source", "unknown")
            title = citation.get("title", "Untitled")
            page = citation.get("page_number", "N/A")
            source_id = citation.get("source_id", "N/A")
            content = chunk.get("content", "").strip()

            context_parts.append(
                f"[Source {index}]\n"
                f"Source: {source}\n"
                f"Title: {title}\n"
                f"Page: {page}\n"
                f"Source ID: {source_id}\n"
                f"Content:\n{content}"
            )

        return "\n\n".join(context_parts)