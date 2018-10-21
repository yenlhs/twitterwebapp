from flask import Flask, jsonify,render_template
from twitterapi import tweepy_streamer


app = Flask(__name__)

@app.route('/')
def index():
    twitter_client = tweepy_streamer.TwitterClient('pycon')
    data = twitter_client.get_user_timeline_tweets(1)
    return render_template("index.html", tweets=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0",port="80", debug=True)