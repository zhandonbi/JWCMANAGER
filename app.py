import json

from flask import Flask, request

from InoutManager import excelInout
from SafetyControl import SafeCode
from User import Account
from db_operator.op_message import EditMessage
from db_operator.op_message import ReadMessage as Message

app = Flask(__name__)


@app.route('/')
def hello_world():
    return {"status": True}


@app.route('/login/', methods=['POST'])
def login():
    username = request.form['userName']
    password = request.form['password']
    print(request.form)
    res = Account.sign_in(username, password)
    return res


@app.route('/register/', methods=['POST'])
def register():
    username = request.form['userName']
    password = request.form['password']
    res = Account.sign_up(username, password)
    return res


@app.route('/GetList/', methods=['POST'])
def GetList():
    SC = eval(request.form['SafetyCode'])
    print(request.form)
    if SafeCode.check_identity(SC, SC['AccountID']):
        field = request.form['fieldName']
        table = request.form['tableName']
        key = request.form['key']
        value = request.form['value']
        res = {}
        print(1)
        if (key != '' and value != '') or (key == '' and value == ''):
            m = Message()
            res = m.get_list(field, table, key, value)
            m.close_link()
        else:
            res = {'status': False, 'message': '检测到缺失的约束条件'}
        return res
    else:
        return {'status': False, 'message': '400'}


@app.route('/GetLine/', methods=['POST'])
def GetLine():
    SC = eval(request.form['SafetyCode'])
    if SafeCode.check_identity(SC, SC['AccountID']):
        table = request.form['tableName']
        key = request.form['key']
        value = request.form['value']
        res = {}
        if (key != '' and value != '') or (key == '' and value == ''):
            m = Message()
            res = m.get_line(table, key, value)
            m.close_link()
        else:
            res = {'status': False, 'message': '检测到缺失的约束条件'}
        return res
    else:
        return {'status': False, 'message': '400'}


@app.route('/GetGroup/', methods=['POST'])
def GetGroup():
    SC = eval(request.form['SafetyCode'])
    if SafeCode.check_identity(SC, SC['AccountID']):
        m = Message()
        res = m.get_all_group()
        m.close_link()
        return res
    else:
        return {'status': False, 'message': '400'}


@app.route('/GetField/', methods=['POST'])
def GetField():
    SC = eval(request.form['SafetyCode'])
    if SafeCode.check_identity(SC, SC['AccountID']):
        table = request.form['tableName']
        m = Message()
        res = m.get_field(table)
        m.close_link()
        return res
    else:
        return {'status': False, 'message': '400'}


@app.route('/GlobalSearch/', methods=['POST'])
def GlobalSearch():
    SC = eval(request.form['SafetyCode'])
    if SafeCode.check_identity(SC, SC['AccountID']):
        value = request.form['value']
        m = Message()
        res = m.god_search(value)
        m.close_link()
        return res
    else:
        return {'status': False, 'message': '400'}


@app.route('/UploadNewGroup/', methods=['POST'])
def UNG():
    SC = eval(request.form['SafetyCode'])
    if SafeCode.check_identity(SC, SC['AccountID']) and (Account.check_identity(SC['AccountID']) == 0):
        GroupName = request.form['groupName']
        listNameCN = request.form['listNameCN'].split(';')
        messageGroup = json.loads(request.form['messageGroup'])
        print(messageGroup)
        m = EditMessage()
        res = m.creat_group(GroupName, listNameCN, messageGroup)
        m.close_link()
        return res
    else:
        return {'status': False, 'message': '账户认证出错或权限不足'}


@app.route('/insert_record/', methods=['POST'])
def IR():
    SC = eval(request.form['SafetyCode'])
    if SafeCode.check_identity(SC, SC['AccountID']) and (Account.check_identity(SC['AccountID']) == 0):
        table = request.form['tableName']
        newRecord = request.form['newRecord']
        m = EditMessage()
        res = m.insert_group(table, newRecord)
        m.close_link()
        return res
    else:
        return {'status': False, 'message': '账户认证出错或权限不足'}


@app.route('/update_record/', methods=['POST'])
def UM():
    SC = eval(request.form['SafetyCode'])
    if SafeCode.check_identity(SC, SC['AccountID']) and (Account.check_identity(SC['AccountID']) == 0):
        table = request.form['tableName']
        recordID = request.form['ID']
        newRecord = request.form['newRecord']
        m = EditMessage()
        res = m.update_message(table, recordID, newRecord)
        m.close_link()
        return res
    else:
        return {'status': False, 'message': '账户认证出错或权限不足'}


@app.route('/upload_excel/', methods=['POST'])
def UE():
    SC = eval(request.form['SafetyCode'])
    if SafeCode.check_identity(SC, SC['AccountID']) and (Account.check_identity(SC['AccountID']) == 0):
        GroupName = request.form['groupName']
        file = request.files.get('excelFile')
        print(file)
        res = excelInout.read(GroupName, file.read(), 'Sheet1')
        return res
    else:
        return {'status': False, 'message': '账户认证出错或权限不足'}


@app.route('/del_group/', methods=['POST'])
def DG():
    SC = eval(request.form['SafetyCode'])
    if SafeCode.check_identity(SC, SC['AccountID']) and (Account.check_identity(SC['AccountID']) == 0):
        table = request.form['tableName']
        m = EditMessage()
        res = m.del_group(table)
        m.close_link()
        return res
    else:
        return {'status': False, 'message': '账户认证出错或权限不足'}


@app.route('/del_record/', methods=['POST'])
def DR():
    SC = eval(request.form['SafetyCode'])
    if SafeCode.check_identity(SC, SC['AccountID']) and (Account.check_identity(SC['AccountID']) == 0):
        table = request.form['tableName']
        recordID = int(request.form['ID'])
        m = EditMessage()
        res = m.del_records(table, recordID)
        m.close_link()
        return res
    else:
        return {'status': False, 'message': '账户认证出错或权限不足'}


if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run(port=5000, debug=True)
