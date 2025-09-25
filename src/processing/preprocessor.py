import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

stop_words = set(stopwords.words('english'))

def clean_text(text):
    # Removes URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    # Removes mentions and '#' symbol
    text = re.sub(r'\@\w+|\#','', text)
    # Removes punctuation
    text = re.sub(r'[^\w\s]', '', text)
    # Converts to lowercase and tokenizes
    tokens = word_tokenize(text.lower())
    # Removes stopwords
    filtered_tokens = [w for w in tokens if not w in stop_words]
    return " ".join(filtered_tokens) # Returns the cleaned text