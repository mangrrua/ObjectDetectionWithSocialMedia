import threading
from PIL import Image
from io import BytesIO
import requests
import random
from instagram_pack.instagram_api import InstagramAPI
import time

"""
    This class provides get data from mongodb and post data to mongodb with specific time interval,
    and reply instagram posts.
"""
class InstProcess:

    def __init__(self, mongo_api, cnn_model):
        """
        Create instances of instagram api, mongo_api and cnn_model
        Passing parameters to instagram api
        :param mongo_api: MongoDB Operations
        :param cnn_model: For predict image
        """
        self._mongo_api = mongo_api
        self._cnn_model = cnn_model

        self._instagram_api = None

    def start(self):
        """
        This function provides create instance of Instagram Api,
        and start thread to getting data from mongodb with specific time interval.
        """
        self._instagram_api = InstagramAPI(mongo_api=self._mongo_api)
        self._inst_run()

    def _download_img_from_url(self, img_url):
        """
        Download image from given url.
        Request to this url and open image.
        :param img_url: Instagram users post.
        :return: downloaded image
        """
        response = requests.get(img_url)
        img = Image.open(BytesIO(response.content))
        print("Downloaded image from url")
        return img

    def _inst_get_img_info_from_db(self):
        """
        This function gets data from mongodb with specific time interval, and it downlaod image from url,
        and it make comment user's post.
        If unanswered post in mongodb, first of all, get data and passing image to cnn_model.
        Cnn model return prediction result and make comment user's post.
        """
        docs = self._mongo_api.inst_get_no_replied_data()
        if docs is None:
            print("No replied documents in instagram collection...")
        else:
            for doc in docs:
                obj_id = doc['_id']
                post_id = doc['post_id']
                full_name = doc['full_name']
                img_url = doc['img_url']

                img = self._download_img_from_url(img_url)
                img = self._cnn_model.preprocess_img(img)
                prediction = self._cnn_model.predict(img)

                if self._inst_reply_post(post_id=post_id, full_name=full_name, prediction=prediction):
                    self._mongo_api.inst_update_doc_after_replied(obj_id)
                    print("Instagram post have answered...")
                    print("Instagram post have updated...")
                else:
                    print("Instagram post haven't replied...")

    def _inst_run(self):
        """
        This function provides start thread with specific time interval.
        Thread starts each ten seconds.
        This thread calls "_inst_get_img_info_from_db" function.
        :return:
        """
        self._inst_get_img_info_from_db()
        print("run method: ", time.ctime())
        th = threading.Timer(
            10,
            self._inst_run
        )
        th.start()

    def _inst_reply_post(self, post_id, full_name, prediction):
        """
        This function provides reply user post.
        :param post_id: Instagram user post id
        :param full_name: Instagram user full name
        :param prediction: Prediction result to giving cnn_model
        :return: If make comment operation is successful, return True
        """
        # replied_message = "Hello @{}, I think, this is a {}".format(screen_name, prediction_result)
        replied_message = "Hello {}, I think this is a {}".format(full_name, prediction)
        try:
            self._instagram_api.reply_post(post_id=post_id, message=replied_message)
            return True
        except:
            print("Failed while answered to Instagram user.")
            return False
