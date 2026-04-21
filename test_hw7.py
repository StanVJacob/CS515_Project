
import unittest
import hw7


class TestCleanInput(unittest.TestCase):
    def test_clean_input_strips_whitespace(self):
        assert hw7.clean_input("  Hello  ") == "Hello"

    def test_clean_input_edge_cases(self):
        pass


class TestIsSupportedLanguage(unittest.TestCase):
    def test_supported_chinese(self):
        assert hw7.is_supported_language("zh-CN") == True

    def test_is_supported_language_other_cases(self):
        pass


class TestTranslateToChinese(unittest.TestCase):
    def test_translate_hello_to_chinese(self):
        assert hw7.translate_to_chinese("Hello") == "你好"

    def test_translate_to_chinese_other_cases(self):
        pass


class TestTranslateToSpanish(unittest.TestCase):
    def test_translate_hello_to_spanish(self):
        assert hw7.translate_to_spanish("Hello") == "Hola"

    def test_translate_to_spanish_other_cases(self):
        pass


class TestGetSupportedLanguages(unittest.TestCase):
    def test_contains_chinese(self):
        assert "zh-CN" in hw7.get_supported_languages()

    def test_get_supported_languages_other_cases(self):
        pass


if __name__ == "__main__":
    unittest.main()
