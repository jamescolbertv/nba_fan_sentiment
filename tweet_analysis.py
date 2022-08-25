# Import libraries
from auth import api
from functions import clean_text, get_subjectivity, get_polarity
from nba_teams import teams
import os
import json
from requests_oauthlib import OAuth1Session
import requests
import tweepy
from wordcloud import WordCloud
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

# Twitter API creds
consumer_key = api['CONSUMER_KEY']
consumer_secret = api['CONSUMER_SECRET']
access_token = api['ACCESS_TOKEN']
access_token_secret = api['ACCESS_TOKEN_SECRET']
# consumer_key = os.environ.get("CONSUMER_KEY")
# consumer_secret = os.environ.get("CONSUMER_SECRET")
# access_token = os.environ.get("ACCESS_TOKEN")
# access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")

# Create authentication object
authenticate = tweepy.OAuthHandler(consumer_key, consumer_secret)

# Set access token and access token secret
authenticate.set_access_token (access_token, access_token_secret)

# Create the API object while passing in auth information
api = tweepy.API(authenticate, wait_on_rate_limit=True)

# Create a dictionaries and lists to store data
# These 3 lists will be used to create a dataframe containing all tweets, their general sentiment, and what team the tweet
# is associated with. This df will be used to pull the highest sentiment tweet for each team.
tweets = []
polarity_list = []
tweet_team = []

# These two dictionaries act as an intermediary for storing data and as the final destination for the tweet highlights data,
# respectively.
team_highlighted_tweets = {}
tweet_highlights = {}

# This is the main dictionary which will be used to visualize every team and how positively or negatively their fanbase
# feels according to Twitter.
team_fan_sentiment = {}

# Extract 100 tweets per team
for team in teams:
    team_sentiment = 0
    posts = api.search_tweets(q=f"#{teams[team]}", count=20, lang='en')
    # Initialize team_highlighted_tweets dictionary with all teams starting at 0
    team_highlighted_tweets[team] = 0
    for tweet in posts:
        tweets.append(tweet.text)
    
    # Clean tweets of @s, #s, 'RT', and URLs.
    clean_tweets = [clean_text(tweet.text) for tweet in posts]
    for tweet in clean_tweets:
        tweet_polarity = get_polarity(tweet)
        polarity_list.append(tweet_polarity)
        tweet_team.append(team)
        # Add tweet sentiment to running total of team sentiment
        team_sentiment += tweet_polarity
    
    # Assign team sentiment rating to team key in team_fan_sentiment dictionary
    team_fan_sentiment[team] = team_sentiment

# Create the tweet_polarity_df dataframe, which will be used to compare and pull out most positive tweets about every team
tweet_polarity_df = pd.DataFrame(
    {
        'Tweet': tweets,
        'TweetPolarity': polarity_list,
        'TweetTeam': tweet_team
    })

# Iterate through tweet_polarity_df and find most positive tweets about each team. 
# Assign tweet to team key in tweet_highlights dictionary.
for index, row in tweet_polarity_df.iterrows():
    polarity = row['TweetPolarity']
    team = row['TweetTeam']
    tweet = row['Tweet']
    if polarity > team_highlighted_tweets[team]:
        tweet_highlights[team] = tweet

print(tweet_highlights)

print(team_fan_sentiment)

# TODO - VISUALIZE the data! Bar chart showing all teams and the sentiment rating that they have for their team would be 
# ideal. Also, start designing single app web page to display this visualization.
        