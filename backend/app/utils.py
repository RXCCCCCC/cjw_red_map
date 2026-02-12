"""工具函数"""


def success(data=None, msg='ok'):
    return {'code': 0, 'msg': msg, 'data': data}


def error(msg='error', code=-1):
    return {'code': code, 'msg': msg, 'data': None}
