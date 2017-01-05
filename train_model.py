import os
import re

import tensorflow as tf
import tensorflow.python.platform
from tensorflow.python.platform import gfile
import numpy as np
import pandas as pd
import sklearn
from sklearn import cross_validation
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.svm import SVC, LinearSVC

import extract_features
import fetch_images


extract_features.maybe_download_and_extract()
extract_features.create_graph()


images_list = []
labels = []

distinctive_class = 'chinese'

for cuisine in fetch_images.cuisines:

    path = cuisine + '_restaurants'

    for file in os.listdir(path):

        filepath = os.path.abspath(os.path.join(path, file))
        _, extension = os.path.splitext(filepath)

        if extension != '.jpeg':
            continue

        images_list.append(filepath)

        if cuisine == distinctive_class:
            labels.append(1)
        else:
            labels.append(2)


features = extract_features.extract_features(images_list)

x_train, x_test, y_train, y_test = cross_validation.train_test_split(features, labels, test_size = 0.2)

classifier = SVC(kernel='rbf')

classifier.fit(x_train, y_train)

y_predicted = classifier.predict(x_test)

print("Accuracy: {0:0.1f}%".format(accuracy_score(y_test, y_predicted) * 100))
