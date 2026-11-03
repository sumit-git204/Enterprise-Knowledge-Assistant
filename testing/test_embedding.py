from app.embeddings.custom_provider import CustomEmbeddings


provider = CustomEmbeddings()

texts = [
    "The bank investigates unauthorized debit complaints.",
    "Customers must report suspicious transactions.",
]

embeddings = provider.embed_documents(texts)

print("Embedding test passed")
print(f"Number of embeddings: {len(embeddings)}")
print(f"Dimensions: {len(embeddings[0])}")
print(f"First 5 values: {embeddings[0][:5]}")

query_embedding = provider.embed_query(
    "What should customers do about suspicious transactions?"
)

print(f"Query embedding dimensions: {len(query_embedding)}")
