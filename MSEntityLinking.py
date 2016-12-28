# -*- coding: utf-8 -*-
'''
use Microsoft Entity Link API to extract entities from scientific papers.
'''
import httplib, urllib, base64

headers = {
    # Request headers
    'Content-Type': 'text/plain',
    'Ocp-Apim-Subscription-Key': '2b3ce8d8300a4eeea41e628c3f214301',
}

params = urllib.urlencode({
    # Request parameters
    #'selection': '{string}',
    #'offset': '{string}',
})


def entityOffsets(text):
    try:
        conn = httplib.HTTPSConnection('api.projectoxford.ai')
        conn.request("POST", "/entitylinking/v1.0/link?%s" % params, text, headers)
        response = conn.getresponse()
        data = response.read()
        #print(data)
        return data
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))