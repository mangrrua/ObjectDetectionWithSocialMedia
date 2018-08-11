from keras.preprocessing.image import img_to_array
from keras.applications.vgg16 import VGG16
from keras.applications.imagenet_utils import decode_predictions, preprocess_input
from keras.models import load_model
import numpy as np
from PIL import Image

"""
    This class provides find object in image. 
    This class uses VGG16 model for object detection.
"""
class CNNModel:

    def __init__(self):
        """
        Download VGG16 Model from Github
        """
        self._model = VGG16(weights='imagenet')

    def preprocess_img(self, img):
        """
        This function provides prepare image before predict image.
        :param img: Downloaded image from url
        :return: Processed image
        """
        r_img = img.resize((224, 224), Image.ANTIALIAS)
        r_img = img_to_array(r_img)
        r_img = np.expand_dims(r_img, axis=0)

        return preprocess_input(r_img)

    def predict(self, img):
        """
        This function predict object in image with VGG16 model.
        :param img: processed image
        :return: Prediction result (Prediction name and its accuracy)
        """
        predictions = self._model.predict(img)
        labels = decode_predictions(predictions)

        return "{} and it's accuracy {}.".format(labels[0][0][1], round(labels[0][0][2], 3))
