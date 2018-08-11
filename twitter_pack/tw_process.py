import threading
from PIL import Image
from io import BytesIO
import requests
import random
from twitter_pack.twitter_api import TwitterAPI


class TwProcess:

    def __init__(self, mongo_api, cnn_model):
        self._mongo_api = mongo_api
        self._cnn_model = cnn_model
        self._twitter_api = None

    def start(self):
        self._twitter_api = TwitterAPI(mongo_api=self._mongo_api)
        self._twitter_api.start_stream()
        self._tw_run()

    def _download_img_from_url(self, img_url):
        response = requests.get(img_url)
        img = Image.open(BytesIO(response.content))
        print("download")
        return img

    def _select_random_message(self, screen_name, prediction_result):

        messages = [
            "Hello @{}, I think, this is a {}".format(screen_name, prediction_result)
        ]

        return random.choice(messages)

    """
        Twitter Operations
    """

    def _tw_get_img_info_from_db(self):
        docs = self._mongo_api.tw_get_no_replied_data()
        print("abc")
        if docs is None:
            print("No replied documents...")
        else:
            replied_docs = []
            for doc in docs:
                print("doccc")
                obj_id = doc['_id']
                tweet_id = doc['tweet_id']
                screen_name = doc['screen_name']
                img_url = doc['img_url']

                img = self._download_img_from_url(img_url)
                img = self._cnn_model.preprocess_img(img)
                prediction = self._cnn_model.predict(img)

                if self._tw_reply_tweet(tweet_id=tweet_id, screen_name=screen_name, prediction=prediction):
                    replied_docs.append(doc)
                    self._mongo_api.tw_update_doc_after_replied(obj_id)
                else:
                    print("Tweet is not replied...")

    def _tw_run(self, interval=15):
        thread = threading.Timer(
                interval,
                self._tw_run,
                [interval]
            )

        thread.start()
        self._tw_get_img_info_from_db()

    def _tw_reply_tweet(self, tweet_id, screen_name, prediction):

        # replied_message = "Hello @{}, I think, this is a {}".format(screen_name, prediction_result)
        replied_message = self._select_random_message(screen_name, prediction)
        try:
            self._twitter_api.reply_tweet(replied_message, tweet_id)
            print("Tweet answered")
            return True
        except:
            print("Failed while answered to twitter user.")
            return False

