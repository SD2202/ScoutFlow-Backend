from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    NVIDIA_LLM_KEY: str = "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"
    NVIDIA_CHAT_KEY: str = "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"
    NVIDIA_EMBED_KEY: str = "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"
    
    MONGODB_URL: str = "mongodb+srv://Sparsh:SSD@cluster1.wu5egox.mongodb.net/"
    DATABASE_NAME: str = "ai_recruiter"
    
    # Model Routing
    LLM_MODEL: str = "meta/llama-3.1-8b-instruct"
    CHAT_MODEL: str = "mistralai/mistral-7b-instruct-v0.3"
    FALLBACK_MODEL: str = "nvidia/nemotron-4-340b-instruct"
    EMBEDDING_MODEL: str = "nvidia/llama-nemotron-embed-1b-v2"

    class Config:
        env_file = ".env"

settings = Settings()
