# -*- coding: utf-8 -*-
"""
@Time    : 11/13/20 6:36 PM
@Author  : Lucky
@Email   : lucky_soft@163.com
@File    : result.py
@Desc    : common http response result
"""
import json

class ResultCommon:
    def __init__(self):
        self.code = 0
        self.statusCode = 0
        self.message = ''
        self.data = {}

    @classmethod
    def success(self, code = 1, statusCode = 1, message = '操作成功', data = None):
        return {"code": code, "statusCode": statusCode, "message": message, "data": data}

    @classmethod
    def fail(self, code = 0, statusCode = 0, message = '操作失败', data = None):
        return {'code': code, 'statusCode': statusCode, 'message': message, 'data': data}



