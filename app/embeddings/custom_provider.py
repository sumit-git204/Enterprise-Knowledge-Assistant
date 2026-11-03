import os
from typing import List

import requests
from dotenv import load_dotenv
from langchain_core.embeddings import Embeddings


load_dotenv(override=True)


class CustomEmbeddings(Embeddings):
    def __init__(
        self,
        endpoint_url: str | None = None,
        api_key: str | None = None,
        dimensions: int = 746,
    ):
        self.endpoint_url = endpoint_url or os.getenv("API_URL")
        self.api_key = api_key or os.getenv("API_KEY")
        self.dimensions = dimensions

        if not self.endpoint_url:
            raise ValueError("API_URL is not configured")

        if not self.api_key:
            raise ValueError("API_KEY is not configured")

        self.headers = {
            "Content-Type": "application/json",
            "X-API-KEY": self.api_key,
        }

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        if not texts or any(not text.strip() for text in texts):
            raise ValueError("Texts cannot be empty")

        payload = {
            "texts": texts,
            "dimensions": self.dimensions,
        }

        response = requests.post(
            self.endpoint_url,
            headers=self.headers,
            json=payload,
            timeout=60,
        )
        if not response.ok:
            print("Status:", response.status_code)
            print("Response:", response.text)
            response.raise_for_status()

        embeddings = response.json()

        if not isinstance(embeddings, list):
            raise ValueError("Embedding API must return a list of vectors")

        if len(embeddings) != len(texts):
            raise ValueError("Embedding count does not match input count")

        for vector in embeddings:
            if len(vector) != self.dimensions:
                raise ValueError("Embedding dimensions do not match configuration")

        return embeddings

    def embed_query(self, text: str) -> List[float]:
        return self.embed_documents([text])[0]

    def embed_text(self, text: str) -> List[float]:
        return self.embed_query(text)

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        return self.embed_documents(texts)
