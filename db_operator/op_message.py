from db_operator.load_db import *
from SafetyControl import SafeCode
import re


# MESSAGE管理
class Message(object):
    def __init__(self):
        self.db = Load('./config/db_con.json')
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

    def get_field_YX(self, Name):
        sql = 'SELECT FieldList, FieldList_CN FROM AllGroup WHERE Name = "{}"'.format(Name)
        self.cur.execute(sql)
        res = self.cur.fetchall()
        Field_dir = {}
        result = {'status': True, 'Field': Field_dir}
        Field_dir['EN'] = res[0][0]
        Field_dir['CN'] = res[0][1]
        return result

    # 获取指定信息组
    def get_field(self, Name):
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
            print(res)
            lable = self.get_field(table)['Field']
            line_all = {}
            result = {'status': True, 'MessageNum': len(res), 'lines': line_all}
            for i in range(0, len(res)):
                nowLine = {}
                for j, key in zip(range(0, len(res[i])), lable.values()):
                    value = str(res[i][j])
                    if value.find(' ') != -1:
                        value = value.split(' ')
                    nowLine[key] = value
                line_all[str(i)] = nowLine
            return result
        except:
            return {'status': False, 'message': '查询表或者约束关键字不存在'}

    def god_search(self, value):
        if value == '' or value is None:
            return {'status': False, 'message': '确实搜索值'}
        tables = self.get_all_group()['Group']

        numbers = 0
        simple = {}
        all_res = {}
        search_res = {'关键词': value, 'listName': '关键词;搜索数目;Group', 'Group': simple}
        result = {'status': True, 'result': search_res, 'allResult': all_res}
        for key in tables.keys():
            files = self.get_field(key)['Field']
            files_CN = list(files.values())
            files = list(files.keys())
            for nowFile in range(0, len(files)):
                files[nowFile] = 'IFNULL(`{}`,\'\')'.format(files[nowFile])
            files = tuple(files)
            files = str(files).replace('\"', '')
            sql = 'SELECT * FROM {} WHERE Concat{} LIKE "%{}%"'.format(key, files, value)
            self.cur.execute(sql)
            res = self.cur.fetchall()
            now = {}
            now_all = []
            for now_line in res:
                now_all.append(list(now_line))
                now[str(now_line[0])] = now_line[1]
            numbers += len(res)
            all_res[tables[key] + '<{}>'.format(len(res))] = now_all
            simple[tables[key] + '<{}>'.format(len(res))] = now
        search_res['搜索数目'] = numbers

        return result

    def close_link(self):
        self.db.close()
