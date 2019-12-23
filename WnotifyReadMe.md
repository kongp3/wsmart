## 企业微信通知转发接口

### 1.基本信息

* **url**: `/wnotify`
* **method**: `POST`
* **content-type**: `Form`

### 2. Header

* 暂无

### 3. 参数

| 入参名 | 说明 |
|  ---  | ---  |
|msg_type| 消息类型: text,普通文本; markdown,MD格式|
|message| 消息内容|
|receiver| 非必传, 接收者组合参数 json字符串, 不传时会给默认接收者发消息 |
|agent_id| 非必传, 应用agent_id, 可指定某应用发消息, 不传默认tnotify应用 |
|corpsecret| 非必传, 应用Secret, 可指定某应用的Secret, 需要和agent_id一一对应, 不传默认用tnotify的secret |


|receiver字段| 说明 |
| ---     | --- |
| touser  | 非必传, 个人ID为接收者 |
| toparty | 非必传, 部门ID为接收者 |
| totag   | 非必传, 标签ID为接收者 |


|touser| 接收者ID                   |
| ---  | ---                       |
| 常规 |  名字全拼首字母大写          |
| 特殊 |  视实际情况而定             |


|toparty   | 接收者ID | 最终接收人 |
| ---      | ---     | ---       |
|部门名称    | 在管理员后台查看  |可在企业微信组织架构查看最终接收人 |


|totag    | 接收者ID | 最终接收人           |
| ---     | ---     | ---                 |
| 标签要在管理员后台建立|   如下是举例     |  |
| python  | 1       | 所有Py开发           |
| finance | 2       | 财务部               |
| op      | 3       | 运营部               |


```
接收者组合参数
{
  <接收者类型1>: 接收者ID1 |  接收者ID2 | ... |  接收者ID3  
  <接收者类型2>: 接收者ID1 |  接收者ID2 | ... |  接收者ID3
  ...  
}

接收者类型: touser,按用户; toparty,按部门; totag,按标签

例
{
    "touser": "Kongp3" | "XX",
    "toparty": "1" | "2",
    "totag": "1" | "2"
}
```


### 4. Demo

* 普通文本

```
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

```
