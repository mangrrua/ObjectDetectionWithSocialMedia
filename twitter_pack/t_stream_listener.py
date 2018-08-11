from tweepy import StreamListener


class TStreamListener(StreamListener):

    def __init__(self, mongo_api):
        super().__init__()
        self.mongo_api = mongo_api
        print("tstreamlistener")

    def on_status(self, status):
        print(status.text)

        if self.is_key(status):
            img_url = status._json['extended_entities']['media'][0]['media_url']
            tweet_id = status.id
            screen_name = status._json['user']['screen_name']

            self.mongo_api.tw_insert(img_url=img_url, tweet_id=tweet_id, screen_name=screen_name)
            print("aldi")
        else:
            print("Does not found image in twitter message!")

    def on_error(self, status_code):
        print("on error")
        if status_code == 420:
            return False

    def is_key(self, data):
        try:
            data._json['extended_entities']
            return True
        except KeyError:
            return False
