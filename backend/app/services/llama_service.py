import httpx
import json
import re
import asyncio
from typing import Dict, Any
from app.core.config import settings


class LlamaService:
    def __init__(self):
        self.api_key = settings.NVIDIA_LLM_KEY
        self.base_url = "https://integrate.api.nvidia.com/v1/chat/completions"
        self.model = settings.LLM_MODEL  # use: meta/llama-3.1-8b-instruct

    async def execute_brain_task(
        self,
        prompt: str,
        system_prompt: str = "You are an expert recruitment AI. Always return valid JSON."
    ) -> Dict[str, Any]:

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
            "temperature": 0.2,
            "max_tokens": 500  # 🔥 reduced for stability
        }

        # 🔁 RETRY LOGIC
        for attempt in range(2):
            try:
                async with httpx.AsyncClient(timeout=15.0) as client:
                    print(f"⏳ Llama call (attempt {attempt+1})")

                    response = await client.post(
                        self.base_url,
                        headers=headers,
                        json=payload
                    )

                response.raise_for_status()
                result = response.json()

                content = result["choices"][0]["message"]["content"]
                print("✅ Llama response received")

                # 🔥 STRONG JSON EXTRACTION
                return self._safe_parse_json(content)

            except Exception as e:
                print(f"❌ Llama error (attempt {attempt+1}): {str(e)}")
                await asyncio.sleep(1)

        # 🔥 FINAL FALLBACK (CRITICAL)
        print("⚠️ Using fallback response")

        return {
            "match_score": 50,
            "strengths": ["Fallback logic used"],
            "weaknesses": ["LLM unavailable"],
            "explanation": "AI service temporarily unavailable",
            "recommendation_status": "Fallback"
        }

    # 🔥 SAFE JSON PARSER (VERY IMPORTANT)
    def _safe_parse_json(self, text: str) -> Dict[str, Any]:
        try:
            # Remove markdown code blocks if present
            text = re.sub(r"```json|```", "", text).strip()

            # Extract JSON object
            json_match = re.search(r"\{.*\}", text, re.DOTALL)

            if json_match:
                return json.loads(json_match.group())

            return json.loads(text)

        except Exception as e:
            print("⚠️ JSON parsing failed:", str(e))
            print("Raw content:", text)

            return {
                "match_score": 50,
                "strengths": [],
                "weaknesses": [],
                "explanation": "Parsing failed",
                "recommendation_status": "Unknown"
            }


llama_service = LlamaService()