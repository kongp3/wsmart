# -*- coding: utf-8 -*-
import json

from config import CORPSECRET, CORPID
from kernel.markdown_msg import MarkdownMsg
from kernel.text_msg import TextMsg
from kernel.file_msg import FileMsg
from kernel.wrequest import WRequest


class MessageFac(object):
    def __init__(self, message, msty):
        self.message = message
        self.type = msty

    def get_message(self):
        if self.type == 'markdown':
            return MarkdownMsg(content=self.message)
        elif self.type == 'text':
            return TextMsg(content=self.message)
        elif self.type == 'file':
            return FileMsg(media_id=self.message)
        # TODO: 这三种是最常用的, 其他的方式用途不大, 陆续在这里扩展
        else:
            raise Exception('Message type is not supported')


class WExecutor(object):
    def __init__(self):
        pass

    def get_token(self, corpsecret):
        if not corpsecret:
            corpsecret = CORPSECRET

        get_token = WRequest(
            'gettoken?corpsecret={corpsecret}&corpid={corpid}'.format(corpsecret=corpsecret, corpid=CORPID),
            {}
        )
        r = get_token.post()
        token = json.loads(r.content).get('access_token')
        return token

    def build_param(self, receiver, content, agent_id):
        params = {}

        if not receiver:
            raise ValueError('Receiver is needed')
        else:
            receiver = json.loads(receiver)

            if receiver.get("touser"):
                params["touser"] = receiver.get("touser")
            if receiver.get("toparty"):
                params["toparty"] = receiver.get("toparty")
            if receiver.get("totag"):
                params["totag"] = receiver.get("totag")

        if not agent_id:
            raise ValueError('AgentId is needed')
        else:
            params["agentid"] = agent_id

        params["msgtype"] = content.msgtype
        params[content.msgtype] = content.content

        return params

    def send_msg(self, **kwargs):

        message = kwargs.get("message")
        msg_type = kwargs.get("msg_type")
        receiver = kwargs.get("receiver") or None
        agent_id = kwargs.get("agent_id") or None
        corpsecret = kwargs.get("corpsecret") or None

        try:
            token = self.get_token(corpsecret)
            fac = MessageFac(message, msg_type)
            content = fac.get_message()
            params = self.build_param(receiver, content, agent_id)

            sending = WRequest(
                'message/send?access_token={token}'.format(token=token),
                json.dumps(params)
            )
            r = sending.post()
            return r.content
        except Exception as e:
            raise e

    def upload_media(self, **kwargs):
        file_path = kwargs.get("file_path")
        corpsecret = kwargs.get("corpsecret")

        token = self.get_token(corpsecret)
        sending = WRequest(
            'media/upload?access_token={token}&type=file'.format(token=token), {},
            {'media': open(file_path)}
        )
        r = sending.post()
        print json.loads(r.content).get("media_id")
        return json.loads(r.content).get("media_id")

