# Text-to-Speech (TTS) Provider Guide

The TTS system utilizes a **Strategy Pattern** architecture, making it seamless to switch between different TTS providers (e.g., Gemini and Edge TTS).

## 🚀 Quick Start

### Via Service (Recommended)

```python
from app.services.core.tts_service import TTSService

# Generate audio - automatically utilizes the configured provider
audio_url = TTSService.generate_question_audio(
    text="Hello, how are you?",
    question_id=123
)
```

### Switching Providers

Edit your `.env` configuration file:

```env
# Use Gemini TTS (Default)
TTS_PROVIDER=gemini
TTS_GEMINI_VOICE=kore
GOOGLE_API_KEY=your-api-key

# Or use Edge TTS
TTS_PROVIDER=edge
TTS_EDGE_VOICE=th-TH-PremwadeeNeural
```

## ⚙️ Configuration Reference

| Setting            | Default                 | Description                              |
| ------------------ | ----------------------- | ---------------------------------------- |
| `tts_provider`     | `gemini`                | Active TTS provider (`gemini` or `edge`) |
| `tts_gemini_voice` | `kore`                  | Selected Gemini voice                    |
| `tts_edge_voice`   | `th-TH-PremwadeeNeural` | Selected Edge voice                      |
| `tts_audio_dir`    | `audio`                 | Output directory for audio files         |

## ✨ Advantages of this Architecture

- **Easily Configurable**: Switch providers instantly via configuration.
- **Extensible**: Add new providers without altering existing code logic.
- **Clean Architecture**: Strong adherence to decoupling and Type Safety.
