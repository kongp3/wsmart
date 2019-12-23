# -*- coding: utf-8 -*-


class FileMsg(object):
    def __init__(self, **kwargs):
        self.msgtype = 'file'
        self.content = {"media_id": kwargs.get("media_id")}

