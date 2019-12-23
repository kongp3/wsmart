# -*- coding: utf-8 -*-

import requests
from config import QY_HOST


class WRequest(object):
    def __init__(self, api_url, params, files=None):
        self.url = QY_HOST.format(url=api_url)
        self.params = params
        self.files = files

        if isinstance(params, dict):
            print 'param is not json'
            self.headers = {}
        else:
            print 'param is json'
            self.headers = {"Content-Type": 'application/json; charset=utf-8'}

        if self.files:
            self.headers = {"Content-Type": "multipart/form-data"}

    def get(self):
        r = requests.get(self.url, params=self.params, headers=self.headers, verify=False)
        print r.content
        return r

    def post(self):
        r = requests.post(self.url, data=self.params, headers=self.headers, files=self.files, verify=False)
        print r.content
        return r

    def put(self):
        r = requests.put(self.url, data=self.params, headers=self.headers, files=self.files, verify=False)
        print r.content
        return r

    def delete(self):
        import urllib
        r = requests.delete(self.url + '?' + urllib.urlencode(self.params), headers=self.headers, files=self.files, verify=False)
        print r.content
