# Classify meals by cuisine.

- 14 cuisines
- 512 images per cuisine extracted using bing image api
- Support vector machine using "one-against-one" classifiers: http://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html
- Features extracted with pretrained neural network: http://download.tensorflow.org/models/image/imagenet/inception-2015-12-05.tgz
- Cross validation using 20% of train set
- Accuracy = 37.1%

![Confusion matrix](https://github.com/NotImplemented/restaurants_by_cuisine_classifier/blob/master/confusion_cuisine_by_meal.png)
