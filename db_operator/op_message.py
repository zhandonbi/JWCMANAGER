from db_operator.load_db import *
from SafetyControl import SafeCode
import re


# MESSAGE管理
class Message(object):
    def __init__(self):
        self.db = Load('config\\db_con.json')
        self.cur = self.db.get_DB_cur()
        self.operator = self.db.get_DB_operator()
        self.table_All = 'AllGroup'

    # 检查信息组是否存在
    def check_group_or_exits(self, Name):
        sql = 'SELECT ID FROM AllGroup WHERE Name = "{}"'.format(Name)
        self.cur.execute(sql)
        res = self.cur.fetchall()
        if len(res) != 0:
            return True
        else:
            return False

    # 获取指定信息组
    def get_field(self, Name):
        sql = ''
        sql = 'SELECT FieldList, FieldList_CN FROM AllGroup WHERE Name = "{}"'.format(Name)
        self.cur.execute(sql)
        res = self.cur.fetchall()
        Field_dir = {}
        result = {'status': True, 'Field': Field_dir}
        Field = str.split(res[0][0], ';')
        Field_CN = str.split(res[0][1], ';')
        for i in range(0, len(Field)):
            Field_dir[Field[i]] = Field_CN[i]
        return result

    def get_all_group(self):
        sql = 'SELECT Name, Name_CN, FieldList, FieldList_CN FROM AllGroup'
        self.cur.execute(sql)
        res = self.cur.fetchall()
        Group = {}
        result = {'status': True, 'fieldNum': len(res), "Group": Group}
        for i in range(0, len(res)):
            Group[res[i][0]] = res[i][1]
        return result

    # 获取所有或者含有指定字段的信息组组名
    def get_group_list(self, field=''):
        sql = ''
        if field == '':
            sql = 'SELECT Name FROM AllGroup'
        else:
            sql = 'SELECT Name FROM AllGroup WHERE {} LIKE "%{}%"'.format('FieldList', field)
        self.cur.execute(sql)
        res = self.cur.fetchall()
        result = []
        for i in res:
            result.append(i[0])
        return result

    # 获取指定信息组下某一列全部或指定信息
    def get_list(self, field, table, key='', value=''):
        sql = ''
        if key == '' or value == '':
            sql = 'SELECT {} FROM {}'.format(field, table)
        elif key != '' and value != '':
            sql = 'SELECT {} FROM {} WHERE {} = "{}"'.format(field, table, key, value)
        try:
            self.cur.execute(sql)
            res = self.cur.fetchall()
            # 存在信息不全，格式错误，更改处
            result = {'status': True, 'MessageNum': len(res)}
            value = []
            for i in range(0, len(res)):
                str_key = str(res[i][0])
                if (str_key not in value) and (str_key.split(' ') not in value) and (
                        str_key is not None and str_key is not 'None'):
                    if str_key.find(' ') != -1:
                        value.append(str_key.split(' '))
                    else:
                        value.append(str_key)
            result['result'] = value
            return result
        except:
            return {'status': False, 'message': '查询字段或信息组不存在'}

    # 获取指定信息组下全部行或指定行信息
    def get_line(self, table, key='', value=''):
        sql = ''
        if key == '' or value == '':
            sql = 'SELECT * FROM {}'.format(table)
        elif key != '' and value != '':
            sql = 'SELECT * FROM {} WHERE {} LIKE "%{}%"'.format(table, key, value)
        try:
            self.cur.execute(sql)
            res = self.cur.fetchall()
            lable = self.get_field(table)['Field']
            line_all = {}
            result = {'status': True, 'MessageNum': len(res), 'lines': line_all}
            for i in range(0, len(res)):
                nowLine = {}
                for j, key in zip(range(1, len(res[i])), lable.values()):
                    value = str(res[i][j])
                    if value.find(' ') != -1:
                        value = value.split(' ')
                    nowLine[key] = value
                line_all[str(i)] = nowLine
            return result
        except:
            return {'status': False, 'message': '查询表或者约束关键字不存在'}

    def close_link(self):
        self.db.close()
