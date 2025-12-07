"""
Text-to-Speech (TTS) generation module.

This module provides text-to-speech generation capabilities using multiple providers:
- Google Gemini TTS: High-quality neural TTS with multiple voice options
- Microsoft Edge TTS: Free TTS service with support for multiple languages

The module includes:
- Custom exception classes for TTS error handling
- Provider-specific generation functions (generate_gemini_tts, generate_edge_tts)
- Unified interface (generate_tts) for easy provider switching
- WAV file creation utilities for audio output

Example:
    Generate speech using Gemini TTS:
        >>> audio_path = generate_gemini_tts("Hello, world!", api_key="your-key")
    
    Generate speech using Edge TTS (async):
        >>> audio_path = await generate_edge_tts("Hello, world!")
    
    Use unified interface:
        >>> audio_path = await generate_tts("Hello!", provider="gemini", api_key="your-key")
"""
import os
import wave
import logging
import tempfile
from typing import Optional
import edge_tts
from google import genai
from google.genai import types

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='my_app.log',
    filemode='a'
)
logger = logging.getLogger(__name__)


class TTSError(Exception):
    """Base exception for TTS-related errors."""
    pass


class TTSProviderError(TTSError):
    """Exception raised when TTS provider fails."""
    pass


class TTSConfigurationError(TTSError):
    """Exception raised for TTS configuration errors."""
    pass


def _create_wave_file(filename: str, pcm_data: bytes, channels: int = 1,
                      rate: int = 24000, sample_width: int = 2) -> None:
    """
    Create a WAV file from PCM data.

    Args:
        filename (str): Output file path
        pcm_data (bytes): PCM audio data
        channels (int): Number of audio channels (default: 1)
        rate (int): Sample rate (default: 24000)
        sample_width (int): Sample width in bytes (default: 2)

    Raises:
        TTSError: If file creation fails
    """
    try:
        with wave.open(filename, "wb") as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(sample_width)
            wf.setframerate(rate)
            wf.writeframes(pcm_data)
        logger.info("Wave file created successfully: %s", filename)
    except Exception as e:
        logger.error("Failed to create wave file: %s", e)
        raise TTSError(f"Failed to create wave file: {e}") from e


def generate_gemini_tts(
    text: str,
    api_key: Optional[str] = None,
    voice: str = "kore",
    output_path: Optional[str] = None
) -> str:
    """
    Generate speech from text using Google Gemini TTS.

    Args:
        text (str): Text to convert to speech
        api_key (Optional[str]): Google API key. If None, uses GOOGLE_API_KEY from env
        voice (str): Voice name to use (default: "kore"). 
                     Allowed voices: achernar, achird, algenib, algieba, alnilam, aoede, 
                     autonoe, callirrhoe, charon, despina, enceladus, erinome, fenrir, 
                     gacrux, iapetus, kore, laomedeia, leda, orus, puck, pulcherrima, 
                     rasalgethi, sadachbia, sadaltager, schedar, sulafat, umbriel, 
                     vindemiatrix, zephyr, zubenelgenubi
        output_path (Optional[str]): Path to save audio file. If None, creates temp file

    Returns:
        str: Path to the generated audio file

    Raises:
        TTSConfigurationError: If API key is not provided or found in environment
        TTSProviderError: If Gemini TTS generation fails
    """
    # Get API key
    if api_key is None:
        api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        error_msg = "Google API key not provided and GOOGLE_API_KEY not found in environment"
        logger.error(error_msg)
        raise TTSConfigurationError(error_msg)

    # Create output path if not provided
    if output_path is None:
        # fd, output_path = tempfile.mkstemp(suffix=".wav", prefix="gemini_tts_")
        output_path = os.path.abspath("gemini_tts.wav")
        # os.close(fd)

    logger.info("Generating Gemini TTS for text: '%s...' (voice: %s)",
                text[:50], voice)

    try:
        # Initialize client
        client = genai.Client(api_key=api_key)

        # Generate audio
        response = client.models.generate_content(
            model="gemini-2.5-flash-preview-tts",
            contents=text,
            config=types.GenerateContentConfig(
                response_modalities=["AUDIO"],
                speech_config=types.SpeechConfig(
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(
                            voice_name=voice,
                        )
                    )
                ),
            )
        )

        # Extract audio data
        audio_data = response.candidates[0].content.parts[0].inline_data.data

        # Save as WAV file
        _create_wave_file(output_path, audio_data)

        logger.info("Gemini TTS generation successful: %s", output_path)
        return output_path

    except ImportError as e:
        error_msg = f"Failed to import Gemini libraries: {e}"
        logger.error(error_msg)
        raise TTSProviderError(error_msg) from e
    except Exception as e:
        error_msg = f"Gemini TTS generation failed: {e}"
        logger.error(error_msg)
        raise TTSProviderError(error_msg) from e


async def generate_edge_tts(
    text: str,
    voice: str = "th-TH-PremwadeeNeural",
    output_path: Optional[str] = None
) -> str:
    """
    Generate speech from text using Edge TTS (async).

    Args:
        text (str): Text to convert to speech
        voice (str): Voice name to use (default: "th-TH-PremwadeeNeural")
        output_path (Optional[str]): Path to save audio file. If None, creates temp file

    Returns:
        str: Path to the generated audio file

    Raises:
        TTSProviderError: If Edge TTS generation fails
    """
    # Create output path if not provided
    if output_path is None:
        fd, output_path = tempfile.mkstemp(suffix=".mp3", prefix="edge_tts_")
        os.close(fd)

    logger.info("Generating Edge TTS for text: '%s...' (voice: %s)",
                text[:50], voice)

    try:
        # Create communicator
        communicate = edge_tts.Communicate(text, voice)

        # Save audio file
        await communicate.save(output_path)

        logger.info("Edge TTS generation successful: %s", output_path)
        return output_path

    except ImportError as e:
        error_msg = f"Failed to import edge_tts library: {e}"
        logger.error(error_msg)
        raise TTSProviderError(error_msg) from e
    except Exception as e:
        error_msg = f"Edge TTS generation failed: {e}"
        logger.error(error_msg)
        raise TTSProviderError(error_msg) from e


async def generate_tts(
    text: str,
    provider: str = "gemini",
    api_key: Optional[str] = None,
    output_path: Optional[str] = None
) -> str:
    """
    Generate speech from text using the specified TTS provider.

    This is a unified interface that supports multiple TTS providers.

    Args:
        text (str): Text to convert to speech
        provider (str): TTS provider to use ("gemini" or "edge", default: "gemini")
        api_key (Optional[str]): API key for providers that require it (Gemini)
        output_path (Optional[str]): Path to save audio file. If None, creates temp file

    Returns:
        str: Path to the generated audio file

    Raises:
        TTSConfigurationError: If provider is invalid
        TTSProviderError: If TTS generation fails
    """
    provider = provider.lower()

    if provider == "gemini":

        return generate_gemini_tts(
            text=text,
            api_key=api_key,
            output_path=output_path
        )

    if provider == "edge":

        return await generate_edge_tts(
            text=text,
            output_path=output_path
        )

    error_msg = f"Invalid TTS provider: {provider}. Supported providers: 'gemini', 'edge'"
    logger.error(error_msg)
    raise TTSConfigurationError(error_msg)
