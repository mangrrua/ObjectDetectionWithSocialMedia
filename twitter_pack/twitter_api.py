import tweepy
from tweepy import Stream
from twitter_pack.t_stream_listener import TStreamListener


class TwitterAPI:

    def __init__(self, mongo_api):
        self._consumer_key = "DEFINE YOUR CONSUMER KEY"
        self._consumer_secret = "DEFINE YOUR CONSUMER SECRET"
        self._access_key = "DEFINE YOUR ACCESS KEY"
        self._access_secret = "DEFINE YOUR ACCESS SECRET"

        self._tw_api = None
        self._stream_listener = TStreamListener(mongo_api=mongo_api)

    def authentication(self):
        try:
            authh = tweepy.OAuthHandler(self._consumer_key, self._consumer_secret)
            authh.set_access_token(self._access_key, self._access_secret)
            authh.get_authorization_url()
            self._tw_api = tweepy.API(authh)

            print("Connected successful to twitter api...")
            return True
        except tweepy.TweepError:
            print("While failed to connected twitter api...")
            return False

    def start_stream(self):
        my_stream = Stream(auth=self._tw_api.auth, listener=self._stream_listener)
        my_stream.filter(track=['ddist'], async=True)

    def reply_tweet(self, message, tweet_id):
        self._tw_api.update_status(message, tweet_id)
