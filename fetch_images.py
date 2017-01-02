import httplib, urllib, base64

headers = {
    # Request headers
    'Content-Type': 'multipart/form-data',
    'Ocp-Apim-Subscription-Key': '66c7302b20914adc9e700cd374f24744',
}

query = 'chinese+restaurants'

try:
    conn = httplib.HTTPSConnection('api.cognitive.microsoft.com')
    conn.request("POST", "/bing/v5.0/images/search?q=" + query, "{body}", headers)
    response = conn.getresponse()
    data = response.read()
    print(data)

    conn.close()

except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))


