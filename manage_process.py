from twitter_pack.tw_process import TwProcess
from instagram_pack.inst_process import InstProcess
from mongo_api import MongoAPI
from cnn_model import CNNModel


"""
    This class manages instagram and twitter process. 
    First of all, it creates objects of mongo_api and cnn_model,
    and it passes this parameters to process'.
"""
class Manage:

    def __init__(self):
        """
        Create new instance of mongo_api, cnn_model, instagram process and twitter process.
        """
        self._mongo_api = MongoAPI()
        self._cnn_model = CNNModel()
        # self._tw_process = TwProcess(mongo_api=self._mongo_api, cnn_model=self._cnn_model)
        self._inst_process = InstProcess(mongo_api=self._mongo_api, cnn_model=self._cnn_model)

    def start(self):
        """
        If mongodb connection is successfully, starts all process.
        :return: If successful return True
        """
        if self._mongo_api.connect():
            self._inst_process.start()
            # self._tw_process.start()
            return True
        else:
            return False
