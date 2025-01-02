import httpx
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

class LLMInterface:
    def __init__(self):
        self.api_key = os.getenv("HUGGINGFACE_API_KEY")
        self.api_url = "https://api-inference.huggingface.co/models/llama-3.1-8b-instruct"
        self.headers = {"Authorization": f"Bearer {self.api_key}"}

    async def query_llm(self, user_query: str, context: list[str]) -> str:
        """Query the LLM with context and user query"""
        formatted_context = "\n".join(context)
        prompt = (
            f"Context:\n{formatted_context}\n\n"
            f"Question: {user_query}\n\n"
            "Answer based on the context above:"
        )

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    self.api_url,
                    headers=self.headers,
                    json={"inputs": prompt},
                    timeout=30.0
                )
                response.raise_for_status()
                return response.json()[0]["generated_text"]
            except httpx.HTTPError as e:
                return f"Error querying LLM: {str(e)}" 