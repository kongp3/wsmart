# -*- coding: utf-8 -*-
import json
import requests


def md_msg_test():
    '''
    msg的内容自定义, 要遵循企业微信MarkDown语法，是标准MarkDown的子集，语法链接如下

    支持的markdown语法
    目前应用消息中支持的markdown语法是如下的子集：

    1. 标题 （支持1至6级标题，注意#与文字中间要有空格）
        # 标题一
        ## 标题二
        ### 标题三
        #### 标题四
        ##### 标题五
        ###### 标题六
    2. 加粗
        **bold**
    3. 链接
        [这是一个链接](http://work.weixin.qq.com/api/doc)
    4. 行内代码段（暂不支持跨行）
        `code`
    5. 引用
        > 引用文字
    6. 字体颜色(只支持3种内置颜色)
        <font color="info">绿色</font>
        <font color="comment">灰色</font>
        <font color="warning">橙红色</font>
    7. 原链接
        https://work.weixin.qq.com/api/doc#90000/90135/90236/%E6%94%AF%E6%8C%81%E7%9A%84markdown%E8%AF%AD%E6%B3%95
    :return:
    '''

    url = 'http://0.0.0.0:31089/wnotify'
    msg_type = 'text'
    msg = '报错提醒:`哎呀呀` \n' \
          '>**错误详情** \n' \
          '>接    口：/qqqq\n' \
          '> \n' \
          '>详细信息：略略略 \n' \
          '>日　  期：2020年5月18日 \n' \
          '>时　  间：上午9:00-11:00 \n' \
          '> \n' \
          '>请及时处理。 \n' \
          '> \n'
    data = {
        'message': msg, 'msg_type': msg_type,
        "receiver": json.dumps({"touser": "Kongp3"})
    }

    r = requests.post(url, data=data, verify=False)
    print r.content


if __name__ == '__main__':
    md_msg_test()
