import unittest

import hw7


class FakeTranslator:
    def __init__(self, source, target):
        self.source = source
        self.target = target

    def translate(self, text):
        translations = {
            ("Hello", "zh-CN"): "Hello in Chinese",
            ("Hello", "es"): "Hola",
            ("Good night", "es"): "Buenas noches",
        }
        return translations.get((text, self.target), f"{text}:{self.target}")


def fake_translator_factory(source, target):
    return FakeTranslator(source, target)


class TestLanguageManager(unittest.TestCase):
    def setUp(self):
        self.manager = hw7.LanguageManager()

    def test_validate_language_accepts_supported_codes(self):
        self.assertTrue(self.manager.validate_language("zh-CN"))
        self.assertTrue(self.manager.validate_language("es"))

    def test_validate_language_is_case_insensitive(self):
        self.assertTrue(self.manager.validate_language("ZH-CN"))
        self.assertTrue(self.manager.validate_language("ES"))

    def test_validate_language_rejects_invalid_values(self):
        self.assertFalse(self.manager.validate_language("ja"))
        self.assertFalse(self.manager.validate_language(""))
        self.assertFalse(self.manager.validate_language(None))

    def test_get_supported_languages_returns_copy(self):
        languages = self.manager.get_supported_languages()
        languages.append("ja")

        self.assertEqual(self.manager.get_supported_languages(), ["zh-CN", "es"])


class TestTranslationService(unittest.TestCase):
    def setUp(self):
        self.service = hw7.TranslationService(
            translator_factory=fake_translator_factory
        )

    def test_clean_input_strips_whitespace(self):
        self.assertEqual(self.service.clean_input("  Hello  "), "Hello")

    def test_clean_input_handles_non_strings(self):
        self.assertEqual(self.service.clean_input(None), "")
        self.assertEqual(self.service.clean_input(123), "")

    def test_translate_text_returns_expected_chinese_output(self):
        self.assertEqual(
            self.service.translate_text("Hello", "zh-CN"),
            "Hello in Chinese",
        )

    def test_translate_text_returns_expected_spanish_output(self):
        self.assertEqual(self.service.translate_text("Hello", "es"), "Hola")
        self.assertEqual(self.service.translate_text("Good night", "es"), "Buenas noches")

    def test_translate_text_skips_empty_input(self):
        self.assertEqual(self.service.translate_text("   ", "zh-CN"), "")


class TestSubtitleProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = hw7.SubtitleProcessor(
            language_manager=hw7.LanguageManager(),
            translation_service=hw7.TranslationService(
                translator_factory=fake_translator_factory
            ),
        )

    def test_process_subtitle_translates_valid_language(self):
        self.assertEqual(
            self.processor.process_subtitle("Hello", "zh-CN"),
            "Hello in Chinese",
        )

    def test_process_subtitle_normalizes_language_code(self):
        self.assertEqual(self.processor.process_subtitle("Hello", "ES"), "Hola")

    def test_process_subtitle_rejects_unsupported_language(self):
        with self.assertRaises(ValueError):
            self.processor.process_subtitle("Hello", "ja")


class TestFunctionWrappers(unittest.TestCase):
    def test_clean_input_wrapper(self):
        self.assertEqual(hw7.clean_input("  Hello  "), "Hello")

    def test_is_supported_language_wrapper(self):
        self.assertTrue(hw7.is_supported_language("zh-cn"))
        self.assertFalse(hw7.is_supported_language("fr"))

    def test_get_supported_languages_wrapper(self):
        self.assertEqual(hw7.get_supported_languages(), ["zh-CN", "es"])


if __name__ == "__main__":
    unittest.main()
