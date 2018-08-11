from pymongo import MongoClient
from pymongo import errors

"""
    Define mongodb uri and db port for connect to mongodb.
"""
MONGO_URI = "YOUR_MONGO_URI"
DB_PORT = 27017

"""
    This class provides use mongodb for store data.
"""
class MongoAPI:

    def __init__(self):
        """
        Define collection names
        """
        self._db_name = "YOUR_DB_NAME"
        self._col_tw_img_inf_name = "YOUR_COLLECTION_NAME"
        self._col_inst_img_inf_name = "YOUR_COLLECTION_NAME"
        self._col_logs_name = "logs"

        self._client = None
        self._db = None
        self._col_tw_img_inf = None
        self._col_inst_img_inf = None
        self._col_logs = None

    def connect(self):
        """
        This function provides connect to mongodb
        Create client, db and collections for use database.
        :return: If connection is successful, return True
        """
        try:
            self._client = MongoClient(MONGO_URI, DB_PORT)
            self._db = self._client[self._db_name]
            self._col_tw_img_inf = self._db[self._col_tw_img_inf_name]
            self._col_inst_img_inf = self._db[self._col_inst_img_inf_name]
            self._col_logs = self._db[self._col_logs_name]

            print("Connected successful to MongoDB server..")
            return True

        except errors.ConnectionFailure:
            print("Could not connect to MongoDB server...")
            return False

    """
        Instagram Operations
    """
    def inst_insert(self, img_url, post_id, full_name):
        """
        Insert instagram post to mongodb
        :param img_url: Instagram user image
        :param post_id: Instagram post id
        :param full_name: Instagram user's full name
        :return: If insert operation is successfull, return True
        """
        data = {
            "img_url": img_url,
            "post_id": post_id,
            "full_name": full_name,
            "is_replied": "No"
        }

        try:
            self._col_inst_img_inf.insert(data)
            return True
        except errors.OperationFailure:
            print("Error for insert data to DB instagram")
            return False

    def inst_is_document_exist(self, post_id):
        """
        This function check document whether exits or not.
        :param post_id: Instagram post id
        :return: If operation is successful, return True
        """
        query = {
            "post_id": post_id
        }

        try:
            count = self._col_inst_img_inf.find(query).count()
            if count > 0:
                return True
            else:
                return False
        except errors.OperationFailure:
            print("op failure")
            return False

    def inst_get_no_replied_data(self):
        """
        This function return unanswered instagram posts in mongodb.
        :return: If there is any unanswered document in mongodb and operation is successful return docs
        """
        query = {
            "is_replied": "No"
        }

        try:
            return list(self._col_inst_img_inf.find(query))
        except errors.OperationFailure:
            print("Error for get no replied data instagram")

    # def inst_update_docs_after_replied(self):
    #     find_query = {
    #         "is_replied": "No"
    #     }
    #
    #     update_query = {
    #         "$set": {
    #             "is_replied": "Yes"
    #         }
    #     }
    #
    #     try:
    #         self._col_inst_img_inf.update_many(find_query, update_query)
    #         return True
    #     except errors.OperationFailure:
    #         print("Error for update docs after replied data instagram")
    #         return False

    def inst_update_doc_after_replied(self, doc_id):
        """
        This function provides update replied document in mongodb
        :param doc_id: Replied document id
        :return: If operation is successful, return True
        """
        find_query = {
            "_id": doc_id
        }

        update_query = {
            "$set": {
                "is_replied": "Yes"
            }
        }

        try:
            self._col_inst_img_inf.update_many(find_query, update_query)
        except errors.OperationFailure:
            print("Error for update doc(!) after replied data instagram")


    """
        Twitter Operations
    """
    def tw_insert(self, img_url, tweet_id, screen_name):
        data = {
            "img_url": img_url,
            "tweet_id": tweet_id,
            "screen_name": screen_name,
            "is_replied": "No"
        }

        try:
            self._col_tw_img_inf.insert(data)
            return True
        except errors.OperationFailure:
            print("Error for insert data to DB")
            return False

    def tw_get_no_replied_data(self):
        query = {
            "is_replied": "No"
        }

        try:
            return list(self._col_tw_img_inf.find(query))
        except errors.OperationFailure:
            print("Error for get no replied data")

    def tw_update_docs_after_replied(self):
        find_query = {
            "is_replied": "No"
        }

        update_query = {
            "$set": {
                "is_replied": "Yes"
            }
        }

        try:
            self._col_tw_img_inf.update_many(find_query, update_query)
            return True
        except errors.OperationFailure:
            print("Error for update docs after replied data")
            return False

    def tw_update_doc_after_replied(self, doc_id):
        find_query = {
            "_id": doc_id
        }

        update_query = {
            "$set": {
                "is_replied": "Yes"
            }
        }

        try:
            self._col_tw_img_inf.update_many(find_query, update_query)
        except errors.OperationFailure:
            print("Error for update doc(!) after replied data")

