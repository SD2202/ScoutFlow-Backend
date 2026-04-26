import httpx
import json
from typing import Dict, Any
from app.core.config import settings

class MistralService:
    def __init__(self):
        self.api_key = settings.NVIDIA_CHAT_KEY
        self.base_url = "https://integrate.api.nvidia.com/v1/chat/completions"
        self.model = settings.CHAT_MODEL # mistralai/mistral-7b-instruct-v0.3

    async def simulate_chat(self, prompt: str, system_prompt: str = "You are a professional candidate responding to a recruiter.") -> Dict[str, Any]:
        """
        Conversational simulation function.
        Uses the NVIDIA_CHAT_KEY.
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7, # Higher temperature for natural chat
            "max_tokens": 512
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(self.base_url, headers=headers, json=payload, timeout=30.0)
            response.raise_for_status()
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            
            # Usually we want JSON for simulated replies to include tone/interest
            if "JSON" in prompt:
                return json.loads(content)
            return {"response": content}

mistral_service = MistralService()
