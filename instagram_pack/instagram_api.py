import requests
import threading
import time


"""
    This function provides get data from instagram server and post data to ınstagram user.
    This class uses the instagram api with access token.
"""
class InstagramAPI:

    def __init__(self, mongo_api):
        """
        Define base instagram api url and access token for connecting instagram bot account.
        :param mongo_api:
        """
        self._base_url = "https://api.instagram.com/v1"
        self._access_token = "DEFINE YOUR ACCESS TOKEN"
        self._tag_name = "ddist"

        self._mongo_api = mongo_api
        self._start()

    def _start(self):
        """
        This function provides start thread with specific time interval.
        Thread starts each ten seconds.
        This thread calls "_get_imgs_from_instagram_posts" function.
        :return:
        """
        print("get images: ", time.ctime())
        self._get_imgs_from_instagram_posts()
        th1 = threading.Timer(
            22,
            self._start
        )
        th1.start()

    def _get_imgs_from_instagram_posts(self):
        """
        This function provides get data from instagram with specific tag and url.
        Function save data to mongodb after getting data (If this data does not exist in mongodb).
        """
        url = "{}/tags/{}/media/recent?access_token={}&count={}".format(self._base_url,
                                                                        self._tag_name,
                                                                        self._access_token, 1)
        try:
            res = requests.get(url)
            returned_data = res.json()

            for data in returned_data['data']:
                img_url = data['images']['standard_resolution']['url']
                post_id = data['id']
                full_name = data['user']['full_name']
                # print(img_url)

                if self._mongo_api.inst_is_document_exist(post_id=post_id): # If document exists in MongoDB
                    print("This instagram post already exist in MongoDB")
                else:
                    self._mongo_api.inst_insert(img_url=img_url, post_id=post_id, full_name=full_name)
                    print("Instagram Post inserted to MongoDB")

        except requests.exceptions.HTTPError:
            print("Request error in get_imgs")

    def reply_post(self, post_id, message):
        """
        This functipn provides send comment to instagram user with url.
        :param post_id: Instagram post id
        :param message: Comment message.
        :return: If operations is successful, return True
        """
        url = "{}/media/{}/comments?access_token={}".format(self._base_url, post_id, self._access_token)
        data = {
            "text": message
        }

        try:
            response = requests.post(url, data=data)
            print("Response after reply post: {}".format(response.text))
            return True
        except requests.exceptions.HTTPError:
            print("Http error while replied instagram post...")
            return False