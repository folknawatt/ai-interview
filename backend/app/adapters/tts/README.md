# TTS Provider Usage Guide

## Overview

The TTS system now uses a flexible **Strategy Pattern** architecture that makes it easy to switch between different TTS providers (Gemini and Edge TTS).

## Quick Start

### Using via Service (Recommended)

```python
from app.services.core.tts_service import TTSService

# Generate audio - automatically uses configured provider
audio_url = TTSService.generate_question_audio(
    text="Hello, how are you?",
    question_id=123
)
print(f"Audio URL: {audio_url}")
```

### Switching Providers

Edit your `.env` file or settings:

```env
# Use Gemini TTS (default)
TTS_PROVIDER=gemini
TTS_GEMINI_VOICE=kore
GOOGLE_API_KEY=your-api-key

# Or use Edge TTS
TTS_PROVIDER=edge
TTS_EDGE_VOICE=th-TH-PremwadeeNeural
```

That's it! No code changes needed.

## Advanced Usage

### Direct Provider Usage

```python
from app.adapters.tts.factory import TTSProviderFactory

# Create Gemini provider
provider = TTSProviderFactory.create_provider(
    "gemini",
    api_key="your-key",
    voice="kore"
)

# Generate audio
audio_path = provider.generate_audio(
    text="สวัสดีครับ",
    output_path="/path/to/output.wav"
)
```

### Create from Settings

```python
from app.adapters.tts.factory import TTSProviderFactory

# Automatically uses settings.tts_provider
provider = TTSProviderFactory.create_from_settings()
audio_path = provider.generate_audio("Hello world")
```

### Using Edge TTS (Async)

```python
from app.adapters.tts.providers import EdgeTTSProvider

provider = EdgeTTSProvider(voice="th-TH-PremwadeeNeural")

# Async usage
audio_path = await provider.generate_audio_async(
    text="สวัสดีครับ",
    output_path="/path/to/output.mp3"
)
```

## Adding a Custom Provider

1. Create a new provider class:

```python
from app.adapters.tts.tts_provider import TTSProvider

class MyCustomTTSProvider(TTSProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_provider_name(self) -> str:
        return "mycustom"

    def generate_audio(
        self,
        text: str,
        output_path: Optional[str] = None,
        **kwargs
    ) -> str:
        # Your implementation here
        pass
```

2. Register the provider:

```python
from app.adapters.tts.factory import TTSProviderFactory

TTSProviderFactory.register_provider("mycustom", MyCustomTTSProvider)
```

3. Use it:

```python
provider = TTSProviderFactory.create_provider(
    "mycustom",
    api_key="your-key"
)
```

## Available Voices

### Gemini Voices

- `kore` (default)
- `charon`, `puck`, `fenrir`
- And 25+ more voices

### Edge Voices

- `th-TH-PremwadeeNeural` (Thai female, default)
- `th-TH-NiwatNeural` (Thai male)
- `en-US-JennyNeural` (English female)
- And 100+ more voices

## Configuration Reference

### Settings

| Setting             | Type | Default                   | Description                                  |
| ------------------- | ---- | ------------------------- | -------------------------------------------- |
| `tts_provider`      | str  | `"gemini"`                | Active TTS provider (`"gemini"` or `"edge"`) |
| `tts_gemini_voice`  | str  | `"kore"`                  | Gemini voice name                            |
| `tts_edge_voice`    | str  | `"th-TH-PremwadeeNeural"` | Edge voice name                              |
| `tts_max_retries`   | int  | `2`                       | Max retry attempts on failure                |
| `tts_initial_delay` | int  | `1`                       | Initial retry delay in seconds               |
| `tts_audio_dir`     | str  | `"audio"`                 | Audio output directory                       |

## Architecture

```
TTSService (Service Layer)
    ↓
TTSProviderFactory (Factory Pattern)
    ↓
TTSProvider (Abstract Base Class)
    ↓
    ├── GeminiTTSProvider
    └── EdgeTTSProvider
```

## Benefits

✅ **Easy Switching** - Change provider with one config setting  
✅ **Extensible** - Add new providers without modifying existing code  
✅ **Testable** - Mock providers for unit testing  
✅ **Clean Code** - Separation of concerns  
✅ **Type Safe** - Full type hints and abstract interfaces
