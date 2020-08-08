import datetime
import hashlib
from db_operator.op_user import User


def get_code(account_id):
    sc = datetime.datetime.now().strftime('%Y%m%d')
    not_md5 = 'acc{}time{}'.format(account_id, sc)
    m = hashlib.md5()
    m.update(bytes(not_md5, encoding="utf8"))
    return {
        'GetTime': sc,
        'AccountID': account_id,
        'SafetyCode': str(m.hexdigest())
    }


def check_identity(SafetyCode, UserName):
    res = User().search_account(UserName)
    if len(res) != 0:
        not_md5 = 'acc{}time{}'.format(res[0][1], SafetyCode['GetTime'])
        m = hashlib.md5()
        m.update(bytes(not_md5, encoding="utf8"))
        if str(m.hexdigest()) == SafetyCode['SafetyCode']:
            return True
        else:
            return False


def update_code(user_name, old_code):
    return old_code


