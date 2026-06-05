"""
memU Factory Configuration Module
==================================

This module provides a production-ready factory for memU Memory instances.
It handles:
- Multi-provider LLM configuration (Ollama, vLLM, OpenRouter, Google, Nvidia NIM)
- Automatic fallback chains between providers on 429/5xx errors
- Environment variable injection for memU internals
- Database connection management
- Error handling and fallback logic

Usage:
------
    from memu_factory import create_memory_instance
    
    # Single provider
    memory = create_memory_instance(
        user_id="admin",
        agent_id="assistant",
        provider="openrouter"
    )
    
    # Multi-provider with automatic fallback
    memory = create_memory_instance(
        user_id="admin",
        agent_id="assistant",
        provider="google",
        enable_fallback=True,  # Activates Nvidia NIM as fallback
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
            "chat_model": "gemini-flash-latest",
            "timeout": 30.0,
            "description": "Google's Gemini models"
        },
        
        "nvidia": {
            "name": "Nvidia NIM",
            "base_url": "https://integrate.api.nvidia.com/v1",
            "api_key": os.getenv("NVIDIA_API_KEY", ""),
            "chat_model": "meta/llama-3.1-8b-instruct",
            "timeout": 30.0,
            "description": "Nvidia NIM (OpenAI-compatible API)"
        }
    }
    
    # STRICT HYBRID SETUP: Always use OpenAI-compatible embeddings (GPT/Gemini via adapter)
    EMBEDDING_PROVIDER = {
        "provider": "google",
        "base_url": "https://generativelanguage.googleapis.com/v1beta",
        "api_key": os.getenv("GOOGLE_API_KEY", ""),
        "model": "gemini-embedding-001",
        "description": "Google AI embeddings (3072 dim)"
    }
    
    MEMORY_FILES_PATH = Path(os.getenv("MEMU_MEMORY_FILES_PATH", "./memory-files"))
    MEMORY_FILES_PATH.mkdir(parents=True, exist_ok=True)
    
    LOG_LEVEL = os.getenv("MEMU_LOG_LEVEL", "INFO")


def create_memory_instance(
    user_id: str = "poweruser_01",
    agent_id: str = "personal_assistant",
    provider: str = "vllm",  # DEFAULT IS NOW vLLM
    custom_config: Optional[Dict[str, Any]] = None,
    enable_fallback: bool = True,
) -> Any:
    """Create a configured memU Memory instance.
    
    Args:
        user_id: User identifier for memory isolation.
        agent_id: Agent identifier (e.g., "personal_assistant").
        provider: Primary LLM provider key from `MemUConfig.PROVIDERS`.
        custom_config: Optional dict of attribute overrides for `MemUConfig`.
        enable_fallback: If True, automatically appends fallback providers
            (Nvidia NIM, vLLM) to the default profile. The fallback chain is
            tried in order whenever the primary returns a 429 or 5xx error.
    
    Returns:
        A fully initialized memU `MemoryService` instance.
    """
    
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
    print(f"   Fallback: {'enabled' if enable_fallback else 'disabled'}")
    
    # Build the default profile from the chosen provider
    default_profile: Dict[str, Any] = {
        "provider": provider,
        "client_backend": "httpx",
        "base_url": provider_config["base_url"],
        "api_key": provider_config["api_key"],
        "chat_model": provider_config["chat_model"],
        "timeout": provider_config["timeout"],
    }
    
    # Add endpoint_overrides for providers that need them
    if provider == "google":
        default_profile["endpoint_overrides"] = {
            "chat": f"models/{provider_config['chat_model']}:generateContent"
        }
    
    # Build the fallback chain if enabled
    fallback_providers: list[Dict[str, Any]] = []
    if enable_fallback:
        fallback_providers = _build_fallback_providers(
            primary=provider,
            config=config,
        )
    if fallback_providers:
        default_profile["fallback_providers"] = fallback_providers
    
    try:
        service = MemoryService(
            llm_profiles={
                "default": default_profile,
                "embedding": {
                    "provider": "google",
                    "client_backend": "httpx",
                    "base_url": config.EMBEDDING_PROVIDER["base_url"],
                    "api_key": config.EMBEDDING_PROVIDER["api_key"],
                    "embed_model": config.EMBEDDING_PROVIDER["model"],
                    "endpoint_overrides": {"embedding": "models/gemini-embedding-001:batchEmbedContents"},
                }
            },
            database_config={
                "metadata_store": {
                    "provider": "postgres",
                    "dsn": config.DATABASE_URL
                }
            },
        )
        
        # Show which providers are in the chain
        if fallback_providers:
            chain = [provider] + [fb.get("provider", "?") for fb in fallback_providers]
            print(f"   Chain: {' -> '.join(chain)}")
        print("✅ Memory Service initialized successfully\n")
        return service
        
    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: {e}")
        print(f"\n💡 Troubleshooting:")
        print(f"   1. Check Docker: docker ps")
        print(f"   2. Check DB: docker exec memu_production_db pg_isready")
        print(f"   3. Verify endpoint: curl {provider_config['base_url']}/models")
        raise


def _build_fallback_providers(
    *,
    primary: str,
    config: Any,
) -> list[Dict[str, Any]]:
    """Build the ordered list of fallback provider configs.
    
    The primary provider is NOT included in the returned list - callers should
    use the primary directly and append the fallbacks. Each fallback is only
    included if the corresponding API key is present in the environment.
    
    Returns:
        List of dicts, each with the same shape as a single LLM profile.
    """
    fallbacks: list[Dict[str, Any]] = []
    
    # Priority order: Nvidia NIM first (OpenAI-compatible, easy swap),
    # then vLLM local as last resort.
    candidate_keys = [
        ("nvidia", "NVIDIA_API_KEY"),
        ("vllm", None),  # vLLM doesn't need an API key
    ]
    
    for prov_key, env_key in candidate_keys:
        if prov_key == primary:
            continue  # Don't duplicate the primary
        prov_cfg = config.PROVIDERS.get(prov_key)
        if not prov_cfg:
            continue
        if env_key and not prov_cfg.get("api_key"):
            continue
        if prov_key == "vllm":
            # Skip vLLM if container isn't running
            import subprocess
            try:
                result = subprocess.run(
                    ["docker", "ps", "--format", "{{.Names}}"],
                    capture_output=True, text=True, timeout=5,
                )
                if "memu_vllm" not in result.stdout:
                    continue
            except Exception:
                continue
        fallback: Dict[str, Any] = {
            "provider": prov_key,
            "client_backend": "httpx",
            "base_url": prov_cfg["base_url"],
            "api_key": prov_cfg.get("api_key", "EMPTY"),
            "chat_model": prov_cfg["chat_model"],
            "timeout": prov_cfg["timeout"],
        }
        if prov_key == "google":
            fallback["endpoint_overrides"] = {
                "chat": f"models/{prov_cfg['chat_model']}:generateContent"
            }
        fallbacks.append(fallback)
    return fallbacks


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
