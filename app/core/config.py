from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    NVIDIA_LLM_KEY: str = ""
    NVIDIA_CHAT_KEY: str = ""
    NVIDIA_EMBED_KEY: str = ""
    
    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "ai_recruiter"
    
    # Model Routing
    LLM_MODEL: str = "meta/llama-3.1-8b-instruct"
    CHAT_MODEL: str = "mistralai/mistral-7b-instruct-v0.3"
    FALLBACK_MODEL: str = "nvidia/nemotron-4-340b-instruct"
    EMBEDDING_MODEL: str = "nvidia/llama-nemotron-embed-1b-v2"

    class Config:
        env_file = ".env"

settings = Settings()
