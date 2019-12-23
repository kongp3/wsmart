# -*- coding: utf-8 -*-
from flask import request, render_template, jsonify

from config import app, CORPID
from application.wclick import WClick
from api import error_handler


@app.route('/wclick', methods=['GET', 'POST'])
@error_handler
def wclick(**kwargs):
    '''
    在企业微信中建立一个应用
    开启API接收功能
    此接口为接收POST请求的主入口
    :param kwargs:
    :return:
    '''
    msg_signature = request.values.get("msg_signature")
    timestamp = request.values.get("timestamp")
    nonce = request.values.get("nonce")

    ec = WClick(corpid=CORPID)
    if request.method == 'GET':
        echo_str = request.values.get("echostr")

        res_str = ec.verify_url(msg_signature, timestamp, nonce, echo_str)
        return res_str

    elif request.method == 'POST':
        req_data = request.data

        msg = ec.decrypt_msg(req_data, msg_signature, timestamp, nonce)
        func = ec.post_dispatch(msg)
        return func(msg=msg)
