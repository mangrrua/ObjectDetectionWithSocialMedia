# ObjectDetectionWithSocialMedia
This project find objects in Instagram and Twitter user's images using CNN.

* Firstly, In this project, images was received from users of social media(Twitter and Instagram) with specific tag. In this way, a lot of images will be collected.
* Secondly, flow of this project; 
  - It receives images of users from Instagram and Twitter, and stores this images to database. 
  - It gets images from mongodb each specific time interval with userID, then finds objects in images, and replies post of users. In the replied comment, predicted object name and its accuracy are written.

----- Requirements -----

* 1- Python 3 
* 2- Numpy
* 3- PIL
* 4- Tensorflow
* 5- Keras
* 6- Flask
* 7- Tweepy (for connect to Twitter api)
* 8- Pymongo

-> If the libraries described above have been successfully installed, you can run this project. Also, you must have a mongodb URI, twitter api keys and instagram access token.

* Optional: If you want use MongoDB on hosted the cloud, you may use Mongo Atlas. For more details; https://www.mongodb.com/cloud/atlas

* Optional: If you want to upload this project to Google App Engine, you must create requirements.txt(libraries described above with its versions) and .yaml file. For more informations, you can see this links; https://cloud.google.com/appengine/docs/standard/python/config/appref
https://cloud.google.com/appengine/docs/flexible/python/using-python-libraries
