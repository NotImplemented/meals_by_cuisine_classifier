import os
import numpy
import urllib
import sys
import tarfile
import tensorflow
import tensorflow.python.platform

from tensorflow.python.platform import gfile

model_url = 'http://download.tensorflow.org/models/image/imagenet/inception-2015-12-05.tgz'
model_directory = 'model'

def maybe_download_and_extract():

    if not os.path.exists(model_directory):
        os.makedirs(model_directory)

    filename = model_url.split('/')[-1]
    filepath = os.path.join(model_directory, filename)

    if not os.path.exists(filepath):

        def progress(count, block_size, total_size):
            sys.stdout.write("\rDownloading '%s': %d%%" % (model_url, 100 * count * block_size / total_size))
            sys.stdout.flush()

        filepath, _ = urllib.request.urlretrieve(model_url, filepath, progress)

        file_info = os.stat(filepath)
        print('Successfully downloaded ', filename, ' (', file_info.st_size, 'bytes).')

    tarfile.open(filepath, 'r:gz').extractall(model_directory)

def create_graph():

    with gfile.FastGFile(os.path.join(model_directory, 'classify_image_graph_def.pb'), 'rb') as file:

        graph_def = tensorflow.GraphDef()
        graph_def.ParseFromString(file.read())

        _ = tensorflow.import_graph_def(graph_def, name='')

def extract_features(images_list):

    feature_dimension = 2048
    features = numpy.empty((len(images_list), feature_dimension))

    with tensorflow.Session() as session:

        flattened_tensor = session.graph.get_tensor_by_name('pool_3:0')

        for i, image_file in enumerate(images_list):

            print('Extracting features from %s...' % image_file)

            if not gfile.Exists(image_file):
                tensorflow.logging.fatal("File '%s' does not exist.", image_file)

            try:
                image_data = gfile.FastGFile(image_file, 'rb').read()
                feature = session.run(flattened_tensor, {'DecodeJpeg/contents:0': image_data})
                features[i, :] = numpy.squeeze(feature)

            except Exception as e:
                print("Error while extracting features from '%s'" % image_file)


    return features

