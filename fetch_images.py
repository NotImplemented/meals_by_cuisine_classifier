import requests
import urllib
import httplib
import time
import json
import os

cuisines = [
    'italian',
    'indian',
    'mexican',
    'thai',
    'chinese',
    'lebanese',
    'greek',
    'japanese',
    'french',
    'spanish',
    'russian',
    'english',
    'turkish',
    'caribbean']

def prepare_data_set():

    headers = {
        # Request headers
        'Content-Type': 'multipart/form-data',
        'Ocp-Apim-Subscription-Key': '66c7302b20914adc9e700cd374f24744',
    }

    sample_size = 512
    batch_size = 128
    retries = 4
    retry_timeout = 4

    for cuisine in cuisines:

        path = cuisine + '_meals'
        try:
            os.makedirs(path)
        except OSError:
            if not os.path.isdir(path):
                raise

        samples_left = sample_size
        offset = 0
        query = cuisine + '+meals'
        index = 0

        print('Preparing data for cuisine: ' + cuisine)

        while samples_left > 0:

            count = min(samples_left, batch_size)
            connection = None

            try:
                connection = httplib.HTTPSConnection('api.cognitive.microsoft.com', timeout = 8)
                request = '/bing/v5.0/images/search?q={}&imageType=Photo&count={}&offset={}'.format(query, count, offset)
                print("Sending request: '{}'".format(request))
                connection.request('POST', request, '{body}', headers)
                response = connection.getresponse()

                data = response.read().decode('utf-8')

                images = json.loads(data)
                images = images['value']

                samples_left -= len(images)
                offset += len(images)

                for image in images:

                    url = image['contentUrl']
                    format = image['encodingFormat']
                    name = '{0}{1:04d}'.format(cuisine, index)

                    location = os.path.join(path, '{name}.{extension}'.format(name = name, extension = format))

                    if not os.path.isfile(location):

                        print('Downloading image #{}: {}'.format(index, url))
                        print('Image location: ' + location)

                        retry = 0
                        response = None
                        while retry < retries :

                            try:
                                response = requests.get(url, timeout = 4)
                                break

                            except requests.exceptions.ConnectionError:
                                print('ConnectionError: Retry #{} downloading image from: {}'.format(retry + 1, url))
                                retry += 1
                                time.sleep(retry_timeout)
                            except requests.exceptions.TooManyRedirects:
                                print('Too many redirects for: {}'.format(url))
                                break
                            except requests.exceptions.ReadTimeout:
                                print('Timeout: Retry #{} downloading image from: {}'.format(retry + 1, url))
                                retry += 1

                        if response and response.status_code == 200:
                            with open(location, 'wb') as file:
                                file.write(response.content)

                    index += 1

            finally:
                if connection:
                    connection.close()
