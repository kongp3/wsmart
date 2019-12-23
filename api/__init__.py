# -*- coding: utf-8 -*-
import traceback
from flask import jsonify
from functools import wraps


class RestResponse(object):
    """ 标准的接口Response类, 所有的api必须返回这个类的对象, 以便统一处理返回 """

    def __init__(self,):
        pass

    def fail(self, code=500, message="Server Got A Exception"):
        d = {'meta': {
            'success': False, 'status_code': code,
            'message': message
        }}
        json_response = jsonify(d, )
        return json_response

    def success(self, code=200, data=None):
        d = {'meta': {
            'success': True, 'status_code': code,
            'message': "Requset Successes"
        }, 'data': data}
        json_response = jsonify(d)
        return json_response


def error_handler(f):
    """
    统一处理异常和返回错误信息, 增加了未知的耦合
    就目前来看还是没问题的
    :param f:
    :return:
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        response = RestResponse()
        try:
            result = f(response=response, *args, **kwargs)
            return result
        except ValueError as e:
            traceback.print_exc(limit=5)
            return response.fail(400, e.message)
        except Exception as e:
            traceback.print_exc(limit=5)
            return response.fail(500, message=e.message)

    return decorated_function
