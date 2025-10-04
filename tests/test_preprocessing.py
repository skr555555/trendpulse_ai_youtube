import pytest
from src.processing.preprocessor import clean_text_multilingual

def test_multilingual_cleaning_english():
    raw_text = "This is a test! Check out https://example.com and follow @user #Awesome"
    expected_text = "check follow awesome"
    assert clean_text_multilingual(raw_text, lang='en') == expected_text

def test_multilingual_cleaning_spanish():
    raw_text = "Este es un coche rápido." # "This is a fast car."
    expected_text = "coche rapido" # "es" and "un" are stopwords
    assert clean_text_multilingual(raw_text, lang='es') == expected_text