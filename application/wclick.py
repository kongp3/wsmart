# -*- coding: utf-8 -*-
from threading import Thread
import xml.etree.cElementTree as ET

from config import AGENTID, CORPSECRET, APP_TOKEN, ENCODING_AES_KEY

from time import time
from application.wwork import WWork

# 定时推送组

# 关键字处理组


class WClick(WWork):

    def __init__(self, **kwargs):
        super(WClick, self).__init__(
            agent_id=AGENTID,
            corpsecret=CORPSECRET,
            token=APP_TOKEN,
            encoding_aes_key=ENCODING_AES_KEY,
            **kwargs)

    def post_dispatch(self, msg):
        '''
        主入口, 做消息细分用
        :param msg:
        :return:
        '''
        xml_tree = ET.fromstring(msg)
        msg_type = xml_tree.find("MsgType")
        if msg_type.text == "event":
            # ''' 事件处理分支 '''
            event_key = xml_tree.find("EventKey").text
            return self.event_dispatch(event_key)
        elif msg_type.text == "text":
            # ''' 回复文本处理分支 '''
            text = xml_tree.find("Content").text
            return self.text_dispatch(text)
        else:
            return self.error_shadow

    def text_dispatch(self, text):
        '''
        消息文本处理
        :param text:
        :return:
        '''

        # TODO: 目前只做了完整匹配和切片匹配, 要多了解下语料库才能把它做成智能, 否则是个智障, 嘻嘻
        if text in ['XXX', 'YYY', 'ZZZ']:
            return self.humer_ai_shadow   # TODO: 这里比较懒都用价值1亿的AI代码敷衍一下咯
        elif text[0:3] in ['XX', 'YY', 'ZZ']:
            return self.humer_ai_shadow
        else:
            return self.humer_ai_shadow

    def event_dispatch(self, event_key):
        '''
        处理点击按钮触发的时间
        按不同的事件类型做分发
        :param event_key:
        :return:
        '''
        if event_key == '子菜单按钮预设的key':
            return self.example_shadow
        elif event_key in ['子菜单跳转的页面链接', '子菜单跳转的页面链接']:
            # TODO: 这里没办法把username传到页面里, 所以通过点击这一事件获取操作人
            # 必要情况下给此人发送消息
            return self.get_username_shadow
        else:
            raise Exception('Unknown Key')

    # --------------- dispatch 和 shadow们的分割线 ---------------------

    def example_shadow(self, **kwargs):
        # shadow作为一个入口, 即使给企业微信服务端response避免超时重新推送
        # 主要代码通过多线程异步方式执行, 执行之后通过send_message方法给操作人反馈
        # 如果处理速度较快可以直接response 但不推荐, 不同环境下处理时间不可控
        msg = kwargs.get("msg")

        xml_tree = ET.fromstring(msg)
        user_name = xml_tree.find("FromUserName").text
        users = {"touser": user_name}

        # ------------收发分割线----------------

        res_data = "<xml><Code>200</Code></xml>"
        encrypt_msg = self.encrypt_msg(res_data)
        start = time()
        t = Thread(target=self.example_report,
                   kwargs={"users": users})
        t.start()
        end = time()
        print end - start
        return encrypt_msg

    def example_report(self, **kwargs):
        users = kwargs.get("users")
        msg = "**我只是一个无公害的Demo**"

        self.send_message(msg, 'markdown', users)

    def error_report(self, **kwargs):
        users = kwargs.get("users")
        self.send_message("对不起，我还识别不了您输入的内容", "markdown", users)

    def error_shadow(self, **kwargs):
        msg = kwargs.get("msg")

        xml_tree = ET.fromstring(msg)
        user_name = xml_tree.find("FromUserName").text
        users = {"touser": user_name}

        # ------------收发分割线----------------

        res_data = "<xml><Code>200</Code></xml>"
        encrypt_msg = self.encrypt_msg(res_data)
        start = time()
        t = Thread(target=self.error_report,
                   kwargs={"users": users})
        t.start()
        end = time()
        print end - start
        return encrypt_msg

    def replay_shadow(self, **kwargs):
        msg = kwargs.get("msg")

        xml_tree = ET.fromstring(msg)
        user_name = xml_tree.find("FromUserName").text
        text = xml_tree.find("Content").text

        # ------------收发分割线----------------
        if text in ["关键字", "key", "key word"]:
            multi_msg = dict(
                title="Title咯",
                description="对, 就这么附言",
                url="https://文章真实路径哦",
                user_name=user_name,
            )
        else:
            self.humer_ai_report(user_name=user_name, text=text)
            res_data = "<xml><Code>200</Code></xml>"
            encrypt_msg = self.encrypt_msg(res_data)
            return encrypt_msg

        return self.replay_report(**multi_msg)

    def replay_report(self, **kwargs):
        '''
        这里是通过Response即时回复和用户交互的demo
        :param kwargs:
        :return:
        '''
        user_name = kwargs.get("user_name")
        title = kwargs.get("title")
        description = kwargs.get("description")
        url = kwargs.get("url")

        # TODO: 这部分有点丑
        res_data = '''  
        <xml>
            <ToUserName><![CDATA[{to_user}]]></ToUserName>
            <FromUserName><![CDATA[{from_user}]]></FromUserName>
            <CreateTime>{create_time}</CreateTime>
            <MsgType><![CDATA[{msg_type}]]></MsgType>
            <ArticleCount>1</ArticleCount>
            <Articles>
                <item>
                    <Title><![CDATA[{title}]]></Title>
                    <Description><![CDATA[{description}]]></Description>
                    <PicUrl><![CDATA[{picurl}]]></PicUrl>
                    <Url><![CDATA[{url}]]></Url>
                </item>
            </Articles>
        </xml>
        '''.format(
            to_user=user_name,
            from_user=user_name,
            create_time=time(),
            msg_type="news",  # TODO: 推送文章的类型这里可以扩展下
            title=title,
            description=description,
            picurl="https://首页图",
            url=url
        )
        encrypt_msg = self.encrypt_msg(res_data)
        return encrypt_msg

    def humer_ai_shadow(self, **kwargs):
        msg = kwargs.get("msg")

        xml_tree = ET.fromstring(msg)
        user_name = xml_tree.find("FromUserName").text
        text = xml_tree.find("Content").text

        # ------------收发分割线----------------

        res_data = "<xml><Code>200</Code></xml>"
        encrypt_msg = self.encrypt_msg(res_data)
        start = time()
        t = Thread(target=self.humer_ai_report,
                   kwargs={"user_name": user_name, "text": text})
        t.start()
        end = time()
        print end - start
        return encrypt_msg

    def humer_ai_report(self, **kwargs):
        '''
        沙雕一下
        这里植入估值一个亿的人工智能[捂脸]
        :param kwargs:
        :return:
        '''
        user_name = kwargs.get("user_name")
        text = kwargs.get("text")

        text = str(text.replace("?", "!"))
        text = str(text.replace("？", "！"))
        text = str(text.replace("吗", ""))

        text = "**{}**".format(text)
        users = {"touser": user_name}
        self.send_message(text, 'markdown', users)

    def get_username_shadow(self, **kwargs):
        msg = kwargs.get("msg")

        xml_tree = ET.fromstring(msg)
        user_name = xml_tree.find("FromUserName").text
        with open('username.txt', 'wb') as f:
            f.write(user_name)
        # ------------收发分割线----------------

        res_data = "<xml><Code>200</Code></xml>"
        encrypt_msg = self.encrypt_msg(res_data)
        return encrypt_msg
