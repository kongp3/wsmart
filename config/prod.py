# -*- coding: utf-8 -*-
from flask import Flask

# NF_HOST = 'https://nf.transfereasy.com'
QY_HOST = "https://qyapi.weixin.qq.com/cgi-bin/{url}"
CORPSECRET = '应用维度的AgentSecret'
CORPID = '企业维度的CorpID'
AGENTID = "应用维度的AgentId"

APP_TOKEN = '应用维度的token用于接口验签'
ENCODING_AES_KEY = '应用维度的key用于接口验签'

app = Flask(__name__)
app_host = '0.0.0.0'
app_port = 31089
