# -*- coding: utf-8 -*-


class TextMsg(object):
    def __init__(self, **kwargs):
        self.msgtype = 'text'
        self.content = {"content": kwargs.get("content")}

