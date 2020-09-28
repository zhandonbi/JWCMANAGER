from SafetyControl.SafeCode import get_code
from db_operator.load_db import *


class __base(object):
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

    def close_link(self):
        self.db.close()


# 读信息
class ReadMessage(__base):
    def __init__(self):
        super().__init__()

    def get_field(self, Name):
        sql = 'SELECT FieldList, FieldList_CN FROM AllGroup WHERE Name = "{}"'.format(Name)
        self.cur.execute(sql)
        res = self.cur.fetchall()
        Field_dir = {}
        result = {'status': True, 'Field': Field_dir}
        Field_dir['EN'] = res[0][0]
        Field_dir['CN'] = res[0][1]
        return result

    # 获取指定信息组
    def __get_field(self, Name):
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
        sql = 'SELECT Name, Name_CN FROM AllGroup'
        self.cur.execute(sql)
        res = self.cur.fetchall()
        Group = {}
        result = {'status': True, 'fieldNum': len(res), "Group": Group}
        for i in range(0, len(res)):
            Group[res[i][1]] = res[i][0]
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
        except Exception as e:
            return {'status': False, 'message': str(e)}

    # 获取指定信息组下全部行或指定行信息
    def get_line(self, table, key='', value=''):
        sql = ''
        if key == '' or value == '':
            sql = 'SELECT * FROM {}'.format(table)
        elif key != '' and value != '':
            sql = 'SELECT * FROM {} WHERE {} = "{}"'.format(table, key, value)
        try:
            self.cur.execute(sql)
            res = self.cur.fetchall()
            lable = self.__get_field(table)['Field']
            line_all = {}
            result = {'status': True, 'MessageNum': len(res), 'lines': line_all}
            for i in range(0, len(res)):
                nowLine = {}
                for j, key in zip(range(0, len(res[i])), lable.values()):
                    value = str(res[i][j])
                    if res[i][j] is None:
                        value = ''
                    value = value.replace(' ', ';')
                    nowLine[key] = value
                line_all[str(i)] = nowLine
            return result
        except Exception as e:
            return {'status': False, 'message': str(e)}

    # 全局搜索
    def god_search(self, value):
        if value == '' or value is None:
            return {'status': False, 'message': '确实搜索值'}
        tables = self.get_all_group()['Group']
        numbers = 0
        simple = {}
        all_res = {}
        search_res = {'关键词': value, 'listName': '关键词;搜索数目;Group', 'Group': simple}
        result = {'status': True, 'result': search_res, 'allResult': all_res}
        for key_CN, key in tables.items():
            files = self.__get_field(key)['Field']
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
            all_res[key_CN + '<{}>'.format(len(res))] = now_all
            simple[key_CN + '<{}>'.format(len(res))] = now
        search_res['搜索数目'] = numbers

        return result


# 编辑
class EditMessage(__base):
    def __init__(self):
        super().__init__()

    def getGroupTable(self, groupName):
        sql1 = 'SELECT Name FROM AllGroup WHERE Name_CN = "{}"'.format(groupName)
        self.cur.execute(sql1)
        res = self.cur.fetchall()
        if len(res) != 0:
            return res[0][0]
        else:
            return None

    def insert_group(self, table, message):
        """
        向已存在信息组插入信息
        """
        try:
            sql1 = 'SELECT FieldList, Name FROM AllGroup WHERE Name="{}"'.format(table)
            self.cur.execute(sql1)
            search = self.cur.fetchall()
            fieldList = search[0][0].split(';')
            if len(message) <= 0:
                return {'status': False, 'message': '传入新条目为空'}
            elif len(message[0]) != (len(fieldList) - 1):
                return {'status': False, 'message': '项目数与传入字段数目不匹配'}
            else:
                tableName = search[0][1]
                value = []
                for m in message:
                    value.append(str(tuple(m)))
                fieldList = str(tuple(fieldList[1:])).replace('\'', '`')
                sql2 = 'INSERT INTO `{}` {} VALUES {}'.format(tableName, fieldList, ','.join(value))
                try:
                    self.cur.execute(sql2)
                    self.operator.commit()
                    return {'status': True, 'message': '添加了{}条记录'.format(len(message))}
                except Exception as e:
                    return {'status': False, 'message': str(e)}
        except Exception as e:
            return {'status': False, 'message': '信息组不存在'}

    def creat_group(self, groupName, listNameCN, messageGroup):
        """
        新建信息组，设计中将内部各类参数设计的较为抽象，避免了外部修改，对照信息存储于AllGroup表中
        """
        # 数据检测
        if len(messageGroup[0]) > len(listNameCN):
            return {'status': False, 'message': '提供对照字段名数目与导入数据不匹配'}
        elif len(messageGroup) <= 0:
            return {'status': False, 'message': '导入数据为空'}
        tableName = get_code(str(messageGroup))['SafetyCode']
        is_exits = self.getGroupTable(groupName)
        if is_exits is not None:
            return {'status': False, 'message': '此内容已存在'}
        else:
            fieldList = []
            str_fl = ''
            for i in range(0, len(listNameCN)):
                fieldList.append('F{}'.format(i))
                str_fl += '`F{}` VARCHAR(40), '.format(i)
            # 表创建
            sql1 = "INSERT INTO AllGroup(Name, Name_CN, ItemNum, FieldList, FieldList_CN) " \
                   "VALUES (\'{}\',\'{}\',{},\'{}\',\'{}\')".format(tableName, groupName, 0,
                                                                    'ID;' + ';'.join(fieldList),
                                                                    '序号;' + ';'.join(listNameCN))
            sql2 = 'CREATE TABLE IF NOT EXISTS `' \
                   + tableName + \
                   '` (`ID` INT UNSIGNED AUTO_INCREMENT, ' \
                   + str_fl + \
                   'PRIMARY KEY (`ID`)' \
                   ')ENGINE=InnoDB DEFAULT CHARSET=utf8'
            self.cur.execute(sql1)
            self.cur.execute(sql2)
            value = []
            for now in messageGroup:
                value.append(str(tuple([str(i) for i in now])))
            fieldList = str(tuple(fieldList)).replace('\'', '`')
            sql3 = 'INSERT INTO `{}` {} VALUES {}'.format(tableName, fieldList, ','.join(value))
            try:
                self.cur.execute(sql3)
                self.operator.commit()
                return {'status': True,
                        'message': '成功创建信息组:{},并插入{}条信息'.format(groupName, len(messageGroup))}
            except Exception as e:
                return {'status': False, 'message': str(e)}

    def update_message(self, table, recordID, newMessage: dict):
        if self.check_group_or_exits(table):
            VALUES = ''
            for key, value in newMessage.items():
                VALUES += '{}="{}"'.format(key, value)
            sql = 'UPDATE {} SET {} WHERE ID={}'.format(table, VALUES, recordID)
            try:
                self.cur.execute(sql)
                self.operator.commit()
                return {'status': True, 'message': '数据修改成功'}
            except Exception as e:
                return {'status': False, 'message': str(e)}
        else:
            return {'status': False, 'message': '查询信息组不存在'}

    def del_group(self, table):
        if self.check_group_or_exits(table):
            sql1 = 'DELETE FROM {} WHERE Name = "{}"'.format('AllGroup', table)
            sql2 = 'DROP TABLE {}'.format(table)
            try:
                self.cur.execute(sql1)
                self.cur.execute(sql2)
                self.operator.commit()
                return {'status': True, 'message': '删除成功'}
            except Exception as e:
                return {'status': False, 'message': str(e)}

        else:
            return {'status': False, 'message': '信息组不存在'}

    def del_records(self, table, recordID):
        if self.check_group_or_exits(table):
            sql = 'DELETE FROM {} WHERE ID = {}'.format(table, recordID)
            try:
                self.cur.execute(sql)
                self.operator.commit()
                return {'status': True, 'message': '删除记录{}成功'.format(recordID)}
            except Exception as e:
                return {'status': False, 'message': str(e)}
        else:
            return {'status': False, 'message': '信息组不存在'}

    def __check(self):
        pass
