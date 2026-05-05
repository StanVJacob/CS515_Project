"""
Backend domain logic for the real-time translator app.

The Flask route should stay thin: it receives JSON and returns JSON. This
module owns input cleanup, language validation, and translation service objects.
"""

from abc import ABC, abstractmethod


SUPPORTED_LANGUAGES = ["zh-CN", "es"]


class LanguageManager:
    """Stores and validates the target languages supported by the app."""

    def __init__(self, supported_languages=None):
        self.supported_languages = list(supported_languages or SUPPORTED_LANGUAGES)

    def get_supported_languages(self):
        return list(self.supported_languages)

    def normalize_language(self, code):
        if not isinstance(code, str):
            return ""

        cleaned_code = code.strip()
        for supported_code in self.supported_languages:
            if supported_code.lower() == cleaned_code.lower():
                return supported_code
        return cleaned_code

    def validate_language(self, code):
        normalized_code = self.normalize_language(code)
        return normalized_code in self.supported_languages


class BaseTranslationService(ABC):
    """Base class for translation services."""

    def clean_input(self, text):
        if not isinstance(text, str):
            return ""
        return text.strip()

    @abstractmethod
    def translate_text(self, text, target_language):
        """Translate text into the requested target language."""


class TranslationService(BaseTranslationService):
    """Google Translator implementation used by the app."""

    def __init__(self, source_language="en", translator_factory=None):
        self.source_language = source_language
        self.translator_factory = translator_factory

    def _create_translator(self, target_language):
        if self.translator_factory:
            return self.translator_factory(
                source=self.source_language,
                target=target_language,
            )

        from deep_translator import GoogleTranslator

        return GoogleTranslator(source=self.source_language, target=target_language)

    def translate_text(self, text, target_language):
        cleaned_text = self.clean_input(text)
        if not cleaned_text:
            return ""

        translator = self._create_translator(target_language)
        return translator.translate(cleaned_text) or ""


class ChineseTranslationService(TranslationService):
    """Specialized translation service for Simplified Chinese."""

    target_language = "zh-CN"

    def translate(self, text):
        return self.translate_text(text, self.target_language)


class SpanishTranslationService(TranslationService):
    """Specialized translation service for Spanish."""

    target_language = "es"

    def translate(self, text):
        return self.translate_text(text, self.target_language)


class BaseSubtitleProcessor(ABC):
    """Base class for processing transcript text into subtitles."""

    @abstractmethod
    def process_subtitle(self, text, target_language="zh-CN"):
        """Return translated subtitle text."""


class SubtitleProcessor(BaseSubtitleProcessor):
    """Coordinates input cleanup, language validation, and translation."""

    def __init__(self, language_manager=None, translation_service=None):
        self.language_manager = language_manager or LanguageManager()
        self.translation_service = translation_service or TranslationService()

    def process_subtitle(self, text, target_language="zh-CN"):
        normalized_language = self.language_manager.normalize_language(target_language)
        if not self.language_manager.validate_language(normalized_language):
            raise ValueError(f"Unsupported language: {target_language}")

        return self.translation_service.translate_text(text, normalized_language)


default_language_manager = LanguageManager()
default_translation_service = TranslationService()
default_subtitle_processor = SubtitleProcessor(
    language_manager=default_language_manager,
    translation_service=default_translation_service,
)


def clean_input(text):
    return default_translation_service.clean_input(text)


def is_supported_language(code):
    return default_language_manager.validate_language(code)


def validate_language(code):
    return default_language_manager.validate_language(code)


def translate_text(text, target_language="zh-CN"):
    return default_subtitle_processor.process_subtitle(text, target_language)


def translate_to_chinese(text):
    return translate_text(text, "zh-CN")


def translate_to_spanish(text):
    return translate_text(text, "es")


def get_supported_languages():
    return default_language_manager.get_supported_languages()
