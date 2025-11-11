from src.translator import translate_content


def test_chinese(monkeypatch):
    original = "这是一条中文消息"
    # Simulate LLM language detection and translation
    monkeypatch.setattr("src.translator.get_language", lambda post: "Chinese")
    monkeypatch.setattr("src.translator.get_translation", lambda post: "This is a Chinese message")

    is_english, translated = translate_content(original)
    assert is_english is False
    assert translated == "This is a Chinese message" 


def test_no_language_recognized(monkeypatch):
    """When language detection returns Unknown, return the original text."""
    original = "🎉🎊🎈"
    monkeypatch.setattr("src.translator.get_language", lambda post: "Unknown")
    monkeypatch.setattr("src.translator.get_translation", lambda post: "(no translation)")

    is_english, translated = translate_content(original)
    assert is_english is False
    assert translated == original


def test_multiple_languages_detected(monkeypatch):
    """When multiple languages are detected, return the original text."""
    mixed = "Hello 世界"
    monkeypatch.setattr("src.translator.get_language", lambda post: "English, Chinese")
    monkeypatch.setattr("src.translator.get_translation", lambda post: "Hello World")

    is_english, translated = translate_content(mixed)
    assert is_english is False
    assert translated == mixed


def test_gibberish_no_language_detected(monkeypatch):
    """Gibberish should return the original when language can't be determined."""
    gibberish = "xyzqwerty asdfgh poiuytrewq"
    monkeypatch.setattr("src.translator.get_language", lambda post: "")
    monkeypatch.setattr("src.translator.get_translation", lambda post: "nonsense")

    is_english, translated = translate_content(gibberish)
    assert is_english is False
    assert translated == gibberish


def test_english_detected(monkeypatch):
    text = "Hello there"
    monkeypatch.setattr("src.translator.get_language", lambda post: "English")
    monkeypatch.setattr("src.translator.get_translation", lambda post: text)

    is_english, translated = translate_content(text)
    assert is_english is True
    assert translated == text