import httpx
import json
from typing import List, Dict, Any, Optional
from app.core.config import settings

class AIService:
    def __init__(self):
        self.base_url = "https://integrate.api.nvidia.com/v1"

    def _get_headers(self, model_type: str) -> Dict[str, str]:
        key = settings.NVIDIA_LLM_KEY
        if model_type == "chat":
            key = settings.NVIDIA_CHAT_KEY
        elif model_type == "embed":
            key = settings.NVIDIA_EMBED_KEY
        
        # Fallback to LLM key if others are empty
        if not key:
            key = settings.NVIDIA_LLM_KEY
            
        return {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"
        }

    async def _post_request(self, endpoint: str, payload: Dict[str, Any], model_type: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/{endpoint}",
                    headers=self._get_headers(model_type),
                    json=payload,
                    timeout=30.0
                )
                response.raise_for_status()
                return response.json()
            except Exception as e:
                # Fallback to Nemotron (using LLM Key) if failure
                if payload.get("model") != settings.FALLBACK_MODEL and model_type != "embed":
                    print(f"Error with {payload.get('model')}, falling back to Nemotron: {str(e)}")
                    payload["model"] = settings.FALLBACK_MODEL
                    return await self._post_request(endpoint, payload, "llm")
                raise e

    async def generate_completion(self, prompt: str, model: str = settings.LLM_MODEL, system_prompt: str = "You are a helpful recruitment assistant.") -> Dict[str, Any]:
        model_type = "chat" if model == settings.CHAT_MODEL else "llm"
        
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2,
            "max_tokens": 1024,
            "response_format": {"type": "json_object"} if "json" in prompt.lower() else None
        }
        
        result = await self._post_request("chat/completions", payload, model_type)
        content = result["choices"][0]["message"]["content"]
        
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return {"raw_text": content}

    async def get_embeddings(self, text: str) -> List[float]:
        payload = {
            "input": [text],
            "model": settings.EMBEDDING_MODEL,
            "input_type": "query"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/embeddings",
                headers=self._get_headers("embed"),
                json=payload,
                timeout=30.0
            )
            response.raise_for_status()
            data = response.json()
            return data["data"][0]["embedding"]

ai_service = AIService()
