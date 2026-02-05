"""
memU Factory Configuration Module
==================================

This module provides a production-ready factory for memU Memory instances.
It handles:
- Multi-provider LLM configuration (Ollama, vLLM, OpenRouter, Google)
- Environment variable injection for memU internals
- Database connection management
- Error handling and fallback logic

Usage:
------
    from memu_factory import create_memory_instance
    
    memory = create_memory_instance(
        user_id="admin",
        agent_id="assistant",
        provider="openrouter"
    )
    
    result = memory.memorize("Important fact")
    context = memory.retrieve("Query", method="rag")
"""

import os
import sys
from pathlib import Path
from typing import Optional, Dict, Any
from dotenv import load_dotenv

load_dotenv()

class MemUConfig:
    """Central configuration class for memU deployment."""
    
    DB_HOST = "127.0.0.1"
    DB_PORT = "5435" # Custom Port
    DB_USER = "memu_admin"
    DB_PASSWORD = os.getenv("DB_PASSWORD", "memu_secure_password_2026")
    DB_NAME = "memu_production" # Default (can be overridden)
    
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    PROVIDERS = {
        "vllm": {
            "name": "vLLM Local Server",
            "base_url": f"{os.getenv('VLLM_HOST', 'http://localhost:8005')}/v1", # Custom Port
            "api_key": "EMPTY",
            "chat_model": "qwen2.5-14b-instruct",
            "timeout": 120.0,
            "description": "Primary: High-performance local serving"
        },

        "ollama": {
            "name": "Ollama Local",
            "base_url": f"{os.getenv('OLLAMA_HOST', 'http://localhost:11434')}/v1",
            "api_key": "ollama",
            "chat_model": "mistral:latest",
            "timeout": 120.0,
            "description": "Backup: Local inference via Ollama"
        },
        
        "openrouter": {
            "name": "OpenRouter Cloud",
            "base_url": "https://openrouter.ai/api/v1",
            "api_key": os.getenv("OPENROUTER_API_KEY", ""),
            "chat_model": "google/gemini-2.0-flash-thinking-exp:free",
            "timeout": 30.0,
            "description": "Cloud inference with multiple models"
        },
        
        "google": {
            "name": "Google AI Studio",
            "base_url": "https://generativelanguage.googleapis.com/v1beta",
            "api_key": os.getenv("GOOGLE_API_KEY", ""),
            "chat_model": "gemini-2.0-flash-exp",
            "timeout": 30.0,
            "description": "Google's Gemini models"
        }
    }
    
    # STRICT HYBRID SETUP: Always use OpenAI-compatible embeddings (GPT/Gemini via adapter)
    EMBEDDING_PROVIDER = {
        "base_url": "https://api.openai.com/v1",
        "api_key": os.getenv("OPENAI_API_KEY", ""),
        "model": "text-embedding-3-small",
        "description": "OpenAI embeddings (Required for 1536 dim)"
    }
    
    MEMORY_FILES_PATH = Path(os.getenv("MEMU_MEMORY_FILES_PATH", "./memory-files"))
    MEMORY_FILES_PATH.mkdir(parents=True, exist_ok=True)
    
    LOG_LEVEL = os.getenv("MEMU_LOG_LEVEL", "INFO")


def create_memory_instance(
    user_id: str = "poweruser_01",
    agent_id: str = "personal_assistant",
    provider: str = "vllm",  # DEFAULT IS NOW vLLM
    custom_config: Optional[Dict[str, Any]] = None
) -> Any:
    """Create a configured memU Memory instance."""
    
    config = MemUConfig()
    
    if provider not in config.PROVIDERS:
        raise ValueError(f"Invalid provider '{provider}'")
    
    provider_config = config.PROVIDERS[provider]
    
    os.environ["OPENAI_API_KEY"] = provider_config["api_key"]
    os.environ["OPENAI_BASE_URL"] = provider_config["base_url"]
    os.environ["OPENAI_API_BASE"] = provider_config["base_url"]
    
    if custom_config:
        for key, value in custom_config.items():
            if hasattr(config, key):
                setattr(config, key, value)
    
    try:
        from memu.app import MemoryService
    except ImportError as e:
        raise ImportError("memU not installed. Run: pip install -e .") from e
    
    print(f"🔧 Initializing memU Memory Service")
    print(f"   User ID: {user_id}")
    print(f"   Agent ID: {agent_id}")
    print(f"   Provider: {provider_config['name']}")
    print(f"   Model: {provider_config['chat_model']}")
    
    try:
        service = MemoryService(
            llm_profiles={
                "default": {
                    "provider": "openai_compatible",
                    "client_backend": "httpx",
                    "base_url": provider_config["base_url"],
                    "api_key": provider_config["api_key"],
                    "chat_model": provider_config["chat_model"],
                    "timeout": provider_config["timeout"],
                },
                "embedding": {
                    "provider": "openai",
                    "base_url": config.EMBEDDING_PROVIDER["base_url"],
                    "api_key": config.EMBEDDING_PROVIDER["api_key"],
                    "embed_model": config.EMBEDDING_PROVIDER["model"],
                }
            },
            database_config={
                "metadata_store": {
                    "provider": "postgres",
                    "connection_string": config.DATABASE_URL
                }
            },
        )
        
        print("✅ Memory Service initialized successfully\n")
        return service
        
    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: {e}")
        print(f"\n💡 Troubleshooting:")
        print(f"   1. Check Docker: docker ps")
        print(f"   2. Check DB: docker exec memu_production_db pg_isready")
        print(f"   3. Verify endpoint: curl {provider_config['base_url']}/models")
        raise


def smoke_test():
    """Quick test to verify configuration."""
    print("=" * 60)
    print("MEMU CONFIGURATION SMOKE TEST")
    print("=" * 60)
    
    config = MemUConfig()
    
    print(f"\n📊 Database: {config.DATABASE_URL.split('@')[1]}")
    print(f"\n🤖 Available Providers:")
    for name, prov in config.PROVIDERS.items():
        status = "✓" if prov["api_key"] else "✗"
        print(f"   {name:12} - {prov['name']:25} {status}")
    print("\n" + "=" * 60)


if __name__ == "__main__":
    smoke_test()
    
    if "--test-init" in sys.argv:
        provider = sys.argv[sys.argv.index("--provider") + 1] if "--provider" in sys.argv else "openrouter"
        memory = create_memory_instance(provider=provider)
        print("✅ Memory instance created!")
