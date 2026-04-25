import asyncio
from openai import AsyncOpenAI
from app.core.config import settings

class EmbeddingService:
    def __init__(self):
        self.api_key = settings.NVIDIA_EMBED_KEY
        self.client = AsyncOpenAI(
            api_key=self.api_key,
            base_url="https://integrate.api.nvidia.com/v1"
        )
        self.model = "nvidia/llama-nemotron-embed-1b-v2"

    async def get_text_embedding(self, text: str):
        if not text or not text.strip():
            print("⚠️ Empty text provided for embedding → using zero vector")
            return [0.0] * 1024

        try:
            response = await self.client.embeddings.create(
                input=[text],
                model=self.model,
                encoding_format="float",
                extra_body={"input_type": "query", "truncate": "NONE"}
            )
            
            # Extract embedding from the OpenAI response object
            return response.data[0].embedding

        except Exception as e:
            print("Embedding Error:", str(e))
            # Fallback to a zero vector of 1024 dimensions (standard for this model)
            return [0.0] * 1024

embedding_service = EmbeddingService()