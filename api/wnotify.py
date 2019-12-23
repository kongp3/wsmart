# -*- coding: utf-8 -*-
from flask import request, jsonify

from config import app
from application.wexecutor import WExecutor
from api import error_handler


@app.route('/wnotify', methods=['POST'])
@error_handler
def wnotify(**kwargs):
    '''
    封装的通知接口
    :param kwargs:
    :return:
    '''
    message = request.values.get('message')
    msg_type = request.values.get('msg_type')
    receiver = request.values.get('receiver')
    agent_id = request.values.get('agent_id')
    corpsecret = request.values.get('corpsecret')

    response = kwargs.get("response")

    we = WExecutor()
    content = we.send_msg(message=message, msg_type=msg_type, receiver=receiver,
                          agent_id=agent_id, corpsecret=corpsecret)
    return response.success()

