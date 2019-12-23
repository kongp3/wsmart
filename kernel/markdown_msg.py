# -*- coding: utf-8 -*-


class MarkdownMsg(object):
    def __init__(self, **kwargs):
        self.msgtype = 'markdown'
        self.content = {"content": kwargs.get("content")}

