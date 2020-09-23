from SafetyControl import SafeCode
from db_operator.op_user import User


# 登陆

def sign_in(username, password):
    u = User()
    res = u.sign_in(username, password)
    if res['status']:
        code = SafeCode.get_code(username)
        res['SafetyCode'] = code
    u.close_link()
    return res


def sign_up(username, password):
    u = User()
    res = u.sign_up(username, password)
    u.close_link()
    return res


def check_identity(username):
    u = User()
    res = u.get_acc_power(username)
    u.close_link()
    return res
