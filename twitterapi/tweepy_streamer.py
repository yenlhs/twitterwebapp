from tweepy.streaming import StreamListener
from tweepy import API
from tweepy import Cursor
from tweepy import OAuthHandler
from tweepy import Stream

import os

class TwitterClient():
    def __init__(self,twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)
        self.twitter_user = twitter_user

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list

    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets


 # # # TWitter AUthenticator
class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        consumerkey = os.environ.get('CONSUMER_KEY')
        consumersecret = os.environ.get('CONSUMER_SECRET')
        accesstoken = os.environ.get('ACCESS_TOKEN')
        accesstokensecret = os.environ.get('ACCESS_TOKEN_SECRET')

        auth = OAuthHandler(consumerkey,consumersecret)
        auth.set_access_token(accesstoken, accesstokensecret)
        return auth


class TwitterStreamer():
    """
    Class for streaming and processing live tweets
    """
    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        """
        This handles Twitter authentication and the connection to the Twitter Streaming API
        """
        listener = TwitterListener(fetched_tweets_filename)
        auth = self.twitter_authenticator.authenticate_twitter_app()
        stream = Stream(auth, listener)
        stream.filter(track=hash_tag_list)

class TwitterListener(StreamListener):
    """
    This is a basic listener class that just print recevied tweets to stdout
    """

    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename
    
    def on_data(self, data):
        """
        override method to manipulate the tweets
        """
        try:
            print(data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on data: %s " % str(e))

    def on_error(self, status):
        if status == 420:
            # Returning false on_data method in case rate limit reached
            return False
        print(status)

if __name__ == '__main__':

    #get user tweets
    twitter_client = TwitterClient('pycon')
    print(twitter_client.get_user_timeline_tweets(1))

    #Stream Tweets based on search keywords
    # hash_tag_list = ['donald trump', 'barak obama']
    # fetched_tweets_filename = "tweets.json"
    # twitter_streamer = TwitterStreamer()
    # twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)


