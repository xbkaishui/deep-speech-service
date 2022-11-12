# encoding: utf-8
import json


class VideoInfo(object):
    url: str
    file_name: str
    callback_url: str

    def __init__(self, url, file_name, callback_url=None):
        self.url = url
        self.file_name = file_name
        self.callback_url = callback_url

    def get_url(self):
        return self.url

    def get_file_name(self):
        return self.file_name

    def get_callback_url(self):
        return self.callback_url

    def set_callback_url(self, url):
        self.callback_url = url


class AudioInfo(object):
    url: str
    file_name: str
    callback_url: str

    def __init__(self, url, file_name, callback_url=None):
        self.url = url
        self.file_name = file_name
        self.callback_url = callback_url

    def get_url(self):
        return self.url

    def get_file_name(self):
        return self.file_name

    def get_callback_url(self):
        return self.callback_url

    def set_callback_url(self, url):
        self.callback_url = url


class Response(object):
    code: int
    data: str

    def __init__(self, code, data):
        self.code = code
        self.data = data

    def to_json(self):
        return json.dumps({"code": self.code, "data": self.data})