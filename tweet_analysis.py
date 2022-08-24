# Import libraries
import os
import json
from requests_oauthlib import OAuth1Session
import requests
import tweepy
from textblob import TextBlob
from wordcloud import WordCloud
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

# Twitter API creds
consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")
access_token = os.environ.get("ACCESS_TOKEN")
access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")

# Create authentication object
authenticate = tweepy.OAuthHandler(consumer_key, consumer_secret)

# Set access token and access token secret
authenticate.set_access_token (access_token, access_token_secret)

# Create the API object while passing in auth information
api = tweepy.API(authenticate, wait_on_rate_limit=True)

# Extract 100 tweets from Twitter user
posts = api.user_timeline(screen_name = "BillGates", count = 100, tweet_mode = "extended")

# Print the last 5 tweets from the account
# print("Show the 5 recent tweets: \n")
posts_list = [tweet.full_text + '\n' for tweet in posts[0:5]]

# for post in posts_list:
#     print(str(posts_list.index(post) + 1) + ') ' + post)

# Create a dataframe with a column called Tweets
df = pd.DataFrame([tweet.full_text for tweet in posts], columns = ['Tweets'])

# Show first 5 rows of data
# print(df.head())

# Clean the text

# Create a function to clean the tweets
def clean_text(text):
    text = re.sub(r'@[A-Za-z0-9_]+', '', text) # Remove @ mentions
    text = re.sub (r'#', '', text) # Remove '#' symbol
    text = re.sub(r'RT[\s]+', '', text) # Remove RT
    text = re.sub(r'https?:\/\/\S+', '', text) # Remove the hyperlink
    
    return text

df['Tweets'] = df['Tweets'].apply(clean_text)

# Show cleaned text
print(df.head())

# Create a function to get subjectivity of tweet (how opinionated tweet is)
def get_subjectivity(text):
    return TextBlob(text).sentiment.subjectivity

# Create a function to get polarity
def get_polarity(text):
    return TextBlob(text).sentiment.polarity

# Create two new columns - subjectivity and polarity
df['Subjectivity'] = df['Tweets'].apply(get_subjectivity)
df['Polarity'] = df['Tweets'].apply(get_polarity)

# Show the new dataframe with new columns
print(df)

# Plot the Word Cloud
all_words = ' '.join([tweets for tweets in df['Tweets']])
word_cloud = WordCloud(width=500, height=300, random_state=21, max_font_size=110).generate(all_words)

plt.imshow(word_cloud, interpolation="bilinear")
plt.axis('off')
plt.show()