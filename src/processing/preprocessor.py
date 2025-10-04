import re
import unicodedata
from nltk.tokenize import word_tokenize
import stopwordsiso as stopwords

def clean_text_multilingual(text, lang='en'):
    """
    A multilingual text cleaning function that handles stopwords and unicode.
    """
    if not isinstance(text, str):
        return ""
        
    # 1. Unicode Normalization
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')

    # 2. Basic Cleaning
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'\@\w+|\#','', text)
    text = re.sub(r'[^\w\s]', '', text)
    
    # 3. Tokenization and Lowercasing
    tokens = word_tokenize(text.lower())
    
    # 4. Multilingual Stopword Removal
    if lang in stopwords.langs():
        stop_words = stopwords.stopwords(lang)
        filtered_tokens = [w for w in tokens if w not in stop_words]
    else:
        # If no stopword list is available, just remove single-character tokens
        filtered_tokens = [w for w in tokens if len(w) > 1]
        
    return " ".join(filtered_tokens)