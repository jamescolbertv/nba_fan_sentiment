import re
from textblob import TextBlob


# CLEAN TEXT
def clean_text(text):
    """
    This function is used to clean the tweets by removing '@' and '#' symbols, as well as RTs and URLs.
    """
    text = re.sub(r'@[A-Za-z0-9_]+', '', text)  # Remove @ mentions
    text = re.sub(r'#', '', text)  # Remove '#' symbol
    text = re.sub(r'RT[\s]+', '', text)  # Remove RT
    text = re.sub(r'https?:\/\/\S+', '', text)  # Remove the hyperlink

    return text

# def get_subjectivity(text):
#     """
#     This function returns subjectivity of a tweet, i.e. how opinionated it is.
#     """
#     return TextBlob(text).sentiment.subjectivity


def get_polarity(text):
    """
    This function returns the polarity of a tweet, i.e. if it's positive or negative.
    """
    return TextBlob(text).sentiment.polarity

def get_analysis(score):
    """
    This function analyzes a score a polarity score and returns either
    'negative', 'neutral' or 'positive'.
    """
    if score < 0:
        return 'Negative'
    elif score == 0:
        return 'Neutral'
    else:
        return 'Positive'
