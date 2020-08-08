from db_operator.load_db import *


# 用户管理
class User(object):
    def __init__(self):
        self.db = Load('config\\db_con.json')
        self.cur = self.db.get_DB_cur()
        self.operator = self.db.get_DB_operator()
        self.table_name = 'user'

    def search_account(self, username):
        sql = 'SELECT ID,user_name FROM {} WHERE user_name = "{}"'.format(self.table_name, username)
        self.cur.execute(sql)
        res = self.cur.fetchall()
        return res

    def check_account_or_exits(self, username: str):
        res = self.search_account(username)
        if len(res) == 0:
            return False
        else:
            return True

    def sign_up(self, username, password):
        # 0-管理员
        # 1-普通用户
        # -1-测试账户
        identity = 1
        sign_status = self.check_account_or_exits(username)
        if sign_status:
            return {
                'status': False,
                'message': '用户已存在'
            }
        else:
            values = '"{}","{}",{}'.format(username, password, identity)
            sql = 'INSERT INTO {} (user_name, password_md5, identity) VALUES ({})'.format(self.table_name, values)
            self.cur.execute(sql)
            self.operator.commit()
            sign_status = self.check_account_or_exits(username)
            if sign_status:
                return {
                    'status': True,
                    'message': '"{}"注册成功'.format(username)
                }
            else:
                return {
                    'status': False,
                    'message': '向服务提交数据失败'
                }

    def sign_in(self, username, password):
        if self.check_account_or_exits(username):
            sql = 'SELECT * FROM {} WHERE user_name = "{}"'.format(self.table_name, username)
            self.cur.execute(sql)
            res = self.cur.fetchall()
            if res[0][2] == password:
                return {
                    'status': True,
                    'UserName': res[0][1],
                    'identity': res[0][3]
                }
            else:
                return {
                    'status': False,
                    'message': '密码错误'
                }
        else:
            return {
                'status': False,
                'message': '{} 不存在'.format(username)
            }

    def close_link(self):
        self.db.close()
