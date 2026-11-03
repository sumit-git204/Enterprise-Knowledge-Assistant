import os

import requests
from dotenv import load_dotenv


load_dotenv(override=True)


class LLMService:
    def __init__(
        self,
        api_url=None,
        model_name=None,
        temperature=0.2,
        top_p=0.9,
        max_tokens=1000,
    ):
        self.api_url = api_url or os.getenv("CHAT_API_URL")
        self.model_name = model_name or os.getenv("CHAT_MODEL_NAME")
        self.api_key = os.getenv("API_KEY")
        self.temperature = temperature
        self.top_p = top_p
        self.max_tokens = max_tokens

        if not self.api_url:
            raise ValueError("CHAT_API_URL is missing")

        if not self.model_name:
            raise ValueError("CHAT_MODEL_NAME is missing")

        if not self.api_key:
            raise ValueError("API_KEY is missing")

    def generate_answer(self, question: str, context: str) -> str:
        question = question.strip()
        context = context.strip()

        if not question:
            raise ValueError("Question cannot be empty")

        if not context:
            return "I couldn't find relevant information in the available documents."

        system_prompt = """
You are an Enterprise Knowledge Assistant.

Answer the user's question using only the evidence provided in the context.

Rules:
1. Do not invent facts or use unsupported external knowledge.
2. If the context does not contain the answer, clearly say that the available
   documents do not provide enough information.
3. Cite evidence using the source labels provided in the context, such as [Source 1].
4. Keep the answer clear, accurate, and concise.
5. If multiple sources support the answer, cite each relevant source.
"""

        user_prompt = f"""
Context:
{context}

Question:
{question}

Provide an evidence-based answer with citations.
"""

        payload = {
            "model": self.model_name,
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            "temperature": self.temperature,
            "top_p": self.top_p,
            "max_tokens": self.max_tokens,
        }

        headers = {
            "Content-Type": "application/json",
            "X-API-KEY": self.api_key,
        }

        response = requests.post(
            self.api_url,
            headers=headers,
            json=payload,
            timeout=90,
        )

        response.raise_for_status()

        data = response.json()

        try:
            answer = data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise ValueError(
                f"Unexpected Quasar chat response format: {data}"
            ) from exc

        if not isinstance(answer, str) or not answer.strip():
            raise ValueError("The LLM returned an empty answer")

        return answer.strip()