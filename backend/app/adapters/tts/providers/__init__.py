"""
TTS provider implementations.

This package contains concrete implementations of the TTSProvider interface.
"""
from app.adapters.tts.providers.gemini_provider import GeminiTTSProvider
from app.adapters.tts.providers.edge_provider import EdgeTTSProvider

__all__ = ["GeminiTTSProvider", "EdgeTTSProvider"]
