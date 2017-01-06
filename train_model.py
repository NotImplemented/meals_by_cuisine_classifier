import os
import numpy

from sklearn import cross_validation
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.svm import SVC
import matplotlib.pyplot as plot

import extract_features
import fetch_images

def plot_confusion_matrix(y_true, y_predicted):

    cm_array = confusion_matrix(y_true, y_predicted)
    true_labels = numpy.unique(y_true)
    predicted_labels = numpy.unique(y_predicted)

    plot.imshow(cm_array[:-1, :-1], interpolation='nearest', cmap=plot.cm.Blues)
    plot.title("Confusion matrix", fontsize=16)
    colorbar = plot.colorbar(fraction=0.046, pad=0.04)
    colorbar.set_label('Number of images', rotation=270, labelpad=30, fontsize=12)

    xtick_marks = numpy.arange(len(true_labels))
    ytick_marks = numpy.arange(len(predicted_labels))

    true_labels_caption = []
    for i in range(len(true_labels)):
        true_labels_caption.append(fetch_images.cuisines[true_labels[i]-1])

    predicted_labels_caption = []
    for i in range(len(true_labels)):
        predicted_labels_caption.append(fetch_images.cuisines[predicted_labels[i]-1])

    plot.xticks(xtick_marks, true_labels_caption, rotation=90)
    plot.yticks(ytick_marks, predicted_labels_caption)
    plot.tight_layout()
    plot.ylabel('True label', fontsize=14)
    plot.xlabel('Predicted label', fontsize=14)

    figure_size = plot.rcParams["figure.figsize"]
    figure_size[0] = 12
    figure_size[1] = 12

    plot.rcParams["figure.figsize"] = figure_size
    plot.show()

extract_features.maybe_download_and_extract()
extract_features.create_graph()

images_list = []
labels = []

for cuisine in fetch_images.cuisines:

    path = cuisine + '_restaurants'

    for file in os.listdir(path):

        file_path = os.path.abspath(os.path.join(path, file))
        _, extension = os.path.splitext(file_path)

        if extension != '.jpeg':
            continue

        images_list.append(file_path)

        labels.append(fetch_images.cuisines.index(cuisine))

features = extract_features.extract_features(images_list)

x_train, x_test, y_train, y_test = cross_validation.train_test_split(features, labels, test_size = 0.2)

classifier = SVC(kernel='rbf')
classifier.fit(x_train, y_train)

y_predicted = classifier.predict(x_test)

print("Accuracy: {0:0.1f}%".format(accuracy_score(y_test, y_predicted) * 100))

plot_confusion_matrix(y_test, y_predicted)

