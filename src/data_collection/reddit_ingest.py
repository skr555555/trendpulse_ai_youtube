import praw
import datetime
from pymongo import MongoClient
from dotenv import load_dotenv
import os

reddit = praw.Reddit(client_id="YOUR_ID",
                    client_secret="YOUR_SECRET",
                     user_agent="TrendPulseCapstone")

client = MongoClient("mongodb://localhost:27017/")
db = client["trendpulse"]
collection = db["reddit_posts"]

def fetch_subreddit(subreddit_name, limit=500):
    for post in reddit.subreddit(subreddit_name).new(limit=limit):
        doc = {
            "id": post.id,
            "title": post.title,
            "text": post.selftext,
            "created_utc": datetime.datetime.utcfromtimestamp(post.created_utc),
            "score": post.score,
            "num_comments": post.num_comments,
            "url": post.url
        }
        collection.insert_one(doc)
