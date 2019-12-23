# -*- coding: utf-8 -*-
import time
import json
import random
from application.wexecutor import WExecutor
from vendor.we_work.callback.WXBizMsgCrypt import WXBizMsgCrypt


class WWork(object):
    def __init__(self, **kwargs):
        self.corpid = kwargs.get("corpid")
        self.agent_id = kwargs.get("agent_id")
        self.corpsecret = kwargs.get("corpsecret")
        self.token = kwargs.get("token")
        self.encoding_aes_key = kwargs.get("encoding_aes_key")

    def verify_url(self, msg_signature, timestamp, nonce, echostr):
        wxcpt = WXBizMsgCrypt(self.token, self.encoding_aes_key, self.corpid)
        ret, echo_str = wxcpt.VerifyURL(msg_signature, timestamp, nonce, echostr)

        if ret != 0:
            raise Exception("ERR: VerifyURL ret: " + str(ret))
        else:
            return echo_str

    def decrypt_msg(self, req_data, msg_signature, timestamp, nonce):
        wxcpt = WXBizMsgCrypt(self.token, self.encoding_aes_key, self.corpid)
        ret, msg = wxcpt.DecryptMsg(req_data, msg_signature, timestamp, nonce)

        if ret != 0:
            raise Exception("ERR: DecryptMsg ret:  " + str(ret))
        else:
            return msg

    def encrypt_msg(self, res_data):
        res_timestamp = str(time.time())
        res_nonce = str(random.randint(1000000000, 9999999999))

        wxcpt = WXBizMsgCrypt(self.token, self.encoding_aes_key, self.corpid)
        ret, encrypt_msg = wxcpt.EncryptMsg(res_data, res_nonce, res_timestamp)
        if ret != 0:
            raise Exception("ERR: EncryptMsg ret: " + str(ret))
        else:
            return encrypt_msg

    def send_message(self, msg, msg_type, users=None):
        we = WExecutor()
        receiver = json.dumps(users)
        content = we.send_msg(message=msg, msg_type=msg_type, receiver=receiver,
                              agent_id=self.agent_id, corpsecret=self.corpsecret)
        return content

    def upload_file(self, file_path):
        we = WExecutor()
        media_id = we.upload_media(file_path=file_path, corpsecret=self.corpsecret)
        return media_id
