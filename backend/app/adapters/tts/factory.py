"""Factory for creating TTS provider instances.

This module implements the Factory pattern to create appropriate
TTS provider instances based on configuration.
"""

from app.adapters.tts.exceptions import TTSConfigurationError
from app.adapters.tts.providers.vachana_provider import VachanaTTSProvider
from app.adapters.tts.tts_provider import TTSProvider
from app.config.logging_config import get_logger
from app.config.settings import settings

logger = get_logger(__name__)


class TTSProviderFactory:
    """Factory for creating TTS provider instances."""

    # Registry of available providers
    _providers = {
        "vachana": VachanaTTSProvider,
    }

    @classmethod
    def create_provider(cls, provider_type: str, **config) -> TTSProvider:
        """Create a TTS provider instance.

        Args:
            provider_type: Type of provider ("vachana")
            **config: Provider-specific configuration parameters
                For Vachana: voice, speed, volume

        Returns:
            TTSProvider: Configured TTS provider instance

        Raises:
            TTSConfigurationError: If provider type is invalid

        Example:
            >>> provider = TTSProviderFactory.create_provider(
            ...     "vachana",
            ...     voice="default"
            ... )
        """
        provider_type = provider_type.lower()

        if provider_type not in cls._providers:
            error_msg = "Invalid TTS provider: %s. Supported providers: %s"
            logger.error(error_msg, provider_type, ", ".join(cls._providers.keys()))
            raise TTSConfigurationError(
                error_msg % (provider_type, ", ".join(cls._providers.keys()))
            )

        provider_class = cls._providers[provider_type]
        logger.info("Creating TTS provider: %s", provider_type)

        try:
            return provider_class(**config)
        except TypeError as e:
            error_msg = "Invalid configuration for %s provider: %s"
            logger.error(error_msg, provider_type, e)
            raise TTSConfigurationError(error_msg % (provider_type, str(e))) from e

    @classmethod
    def create_from_settings(cls) -> TTSProvider:
        """Create a TTS provider from application settings.

        Returns:
            TTSProvider: Configured TTS provider instance

        Raises:
            TTSConfigurationError: If configuration is invalid
        """
        provider_type = settings.tts_provider

        # Prepare provider-specific configuration
        if provider_type == "vachana":
            config = {
                "voice": settings.tts_vachana_voice,
            }
        else:
            config = {}

        return cls.create_provider(provider_type, **config)

    @classmethod
    def register_provider(cls, name: str, provider_class: type) -> None:
        """Register a custom TTS provider.

        This allows developers to add new providers without modifying
        the factory code.

        Args:
            name: Provider name (lowercase)
            provider_class: Provider class (must inherit from TTSProvider)

        Example:
            >>> class CustomTTSProvider(TTSProvider):
            ...     pass
            >>> TTSProviderFactory.register_provider("custom", CustomTTSProvider)
        """
        if not issubclass(provider_class, TTSProvider):
            raise TypeError("Provider class must inherit from TTSProvider")

        cls._providers[name.lower()] = provider_class
        logger.info("Registered custom TTS provider: %s", name)

    @classmethod
    def get_available_providers(cls) -> list[str]:
        """Get list of available provider names.

        Returns:
            list[str]: List of provider names
        """
        return list(cls._providers.keys())
