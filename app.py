from flask import Flask, request
from User import Account
from SafetyControl import SafeCode
from db_operator.op_message import Message

app = Flask(__name__)


@app.route('/')
def hello_world():
    return {"status": True}


@app.route('/login/', methods=['GET', 'POST'])
def login():
    username = request.form['UserName']
    password = request.form['password']
    print(request.form)
    res = Account.sign_in(username, password)
    return res


@app.route('/register/', methods=['POST'])
def register():
    username = request.form['UserName']
    password = request.form['password']
    res = Account.sign_up(username, password)
    return res


@app.route('/GetList/', methods=['POST'])
def GetList():
    SC = eval(request.form['SafetyCode'])
    print(request.form)
    if SafeCode.check_identity(SC, SC['AccountID']):
        field = request.form['FieldName']
        table = request.form['GroupName']
        key = request.form['key']
        value = request.form['value']
        res = {}
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
        table = request.form['GroupName']
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
        GroupName = request.form['GroupName']
        m = Message()
        res = m.get_field(GroupName)
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


@app.route('/GetFieldYX/', methods=['POST'])
def GFYX():
    SC = eval(request.form['SafetyCode'])
    if SafeCode.check_identity(SC, SC['AccountID']):
        GroupName = request.form['GroupName']
        m = Message()
        res = m.get_field_YX(GroupName)
        m.close_link()
        return res
    else:
        return {'status': False, 'message': '400'}


if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run(port=5000)
