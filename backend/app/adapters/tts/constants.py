"""TTS Constants."""

import os

# Audio Configuration
DEFAULT_SAMPLE_RATE = 24000  # Gemini TTS default sample rate
DEFAULT_CHANNELS = 1  # Mono audio
DEFAULT_SAMPLE_WIDTH = 2  # 16-bit audio (2 bytes)

# Gemini TTS Configuration
GEMINI_MODEL = "gemini-2.5-flash-preview-tts"
DEFAULT_GEMINI_VOICE = "kore"

# Available Gemini voices (as of API version)
GEMINI_VOICES = [
    "achernar",
    "achird",
    "algenib",
    "algieba",
    "alnilam",
    "aoede",
    "autonoe",
    "callirrhoe",
    "charon",
    "despina",
    "enceladus",
    "erinome",
    "fenrir",
    "gacrux",
    "iapetus",
    "kore",
    "laomedeia",
    "leda",
    "orus",
    "puck",
    "pulcherrima",
    "rasalgethi",
    "sadachbia",
    "sadaltager",
    "schedar",
    "sulafat",
    "umbriel",
    "vindemiatrix",
    "zephyr",
    "zubenelgenubi",
]

# Edge TTS Configuration
DEFAULT_EDGE_VOICE = "th-TH-PremwadeeNeural"  # Thai female voice

# File Configuration
AUDIO_OUTPUT_DIR = os.path.join("storage", "temp", "audio")
GEMINI_OUTPUT_FILENAME = "gemini_tts.wav"
