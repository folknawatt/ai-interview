# Text-to-Speech (TTS) Provider Guide

The TTS system utilizes a **Strategy Pattern** architecture, making it seamless to switch between different TTS providers if needed in the future. Currently, it is natively configured to use **Vachana TTS**.

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

### Configuration

Edit your `.env` configuration file:

```env
# Use Vachana TTS (Default)
TTS_PROVIDER=vachana
TTS_VACHANA_VOICE=th_f_1
```

## ⚙️ Configuration Reference

| Setting             | Default                | Description                               |
| ------------------- | ---------------------- | ----------------------------------------- |
| `tts_provider`      | `vachana`              | Active TTS provider (`vachana` supported) |
| `tts_vachana_voice` | `th_f_1`               | Selected Vachana voice                    |
| `tts_audio_dir`     | `storage/public/audio` | Output directory for audio files          |

## ✨ Advantages of this Architecture

- **Easily Configurable**: Switch providers instantly via configuration.
- **Extensible**: Add new providers without altering existing code logic.
- **Clean Architecture**: Strong adherence to decoupling and Type Safety.
