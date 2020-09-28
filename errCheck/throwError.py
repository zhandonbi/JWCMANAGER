def checkNone(*args):
    if None in args:
        return {'status': False, 'message': '参数缺失'}
