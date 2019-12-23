# -*- coding: utf-8 -*-
import json
import requests


def txt_msg_test():
    '''
    msg的内容自定义, 不需要遵循任何语法
    这里写成这样是为了和隔壁markdown测试用例做个效果的对比
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
    txt_msg_test()
