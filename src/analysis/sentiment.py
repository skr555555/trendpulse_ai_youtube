import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# The following line is needed only on the first run to download the VADER lexicon.
# You can run this in a Python interpreter or uncomment it for one run.
# try:
#     nltk.data.find('sentiment/vader_lexicon.zip')
# except nltk.downloader.DownloadError:
#     nltk.download('vader_lexicon')

# Initialize the VADER sentiment intensity analyzer once at the module level for efficiency.
sid = SentimentIntensityAnalyzer()

def get_sentiment(text: str) -> str:
    """
    Analyzes the sentiment of a given text using VADER.

    Args:
        text (str): The input text to analyze.

    Returns:
        str: A sentiment label ('Positive', 'Negative', or 'Neutral').
    """
    if not isinstance(text, str):
        return 'Neutral'
        
    # Get the polarity scores which include positive, negative, neutral, and a compound score.
    scores = sid.polarity_scores(text)
    
    # The 'compound' score is a metric that sums up the sentiment scores of each word,
    # normalized between -1 (most extreme negative) and +1 (most extreme positive).
    compound_score = scores['compound']
    
    # Use standard thresholds to classify the sentiment.
    if compound_score >= 0.05:
        return 'Positive'
    elif compound_score <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'