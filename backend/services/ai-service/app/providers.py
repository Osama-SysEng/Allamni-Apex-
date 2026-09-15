"""
Compatibility layer for legacy provider system
This file now uses the new centralized AI provider system
"""
import os
from shared.ai_providers import get_ai_provider, AIProviderType

def get_provider(name=None):
    """Get AI provider instance (legacy compatibility)"""
    provider_type = os.getenv("AI_PROVIDER", "mock")
    
    try:
        return get_ai_provider(
            provider_type=AIProviderType(provider_type),
            api_key=os.getenv("GEMINI_API_KEY"),
            model=os.getenv("GEMINI_MODEL", "gemini-1.5-pro")
        )
    except Exception:
        # Fallback to mock provider if configuration fails
        from shared.ai_providers import MockAIProvider
        return MockAIProvider()
