# 管理系统后台API文档

#### 基本功能介绍：

基本连入链接：http://IP/

#### 具体接口：

1. ##### ‘’（首页链接）

   > 功能：测试与服务器连接状态
   >
   > 请求方式：GET
   >
   > 返回JSON格式数据
   >
   > 返回示例:
   >
   > > ```JSON
   > > {"status": True}//后续返回格式status键值都代表请求执行情况
   > > ```

2. ##### login/

   > 功能：用户登录
   >
   > 请求方式：POST
   >
   > 请求表单form字段
   >
   > ```JSON
   > {
   > 	'UserName'：用户名
   > 	'password'：密码（经过MD5加密后）
   > }
   > ```
   >
   > 返回JSON格式数据
   >
   > 返回示例
   >
   > > ```JSON
   > > //登陆成功
   > > {
   > > 	'status': True, 
   > > 	'UserName': 'test', 		
   > >     	'identity': 1, 	
   > >     // SafetyCode为身份验证信息，用于每次请求检测身份
   > > 	'SafetyCode': {
   > > 		'GetTime': '20200807', 
   > > 		'AccountID': 'test', 
   > > 		'SafetyCode': 'b5f62f9ff6eab9a78906d7318660884d'
   > > 	}
   > > }
   > > //登陆失败
   > > {
   > >     	'status': False, 
   > >     	'message': '密码错误'
   > > }
   > > ```

3. ##### ‘register/’

   > 功能：用户注册
   >
   > 请求方式：POST
   >
   > 请求表单form字段
   >
   > ```JSON
   > {
   > 	'UserName'：用户名
   > 	'password'：密码（经过MD5加密后）
   > }
   > ```
   >
   > 返回JSON格式数据
   >
   > 返回示例
   >
   > ```JSON
   > //注册成功
   > {'status': True, 'message': '"test2"注册成功'}
   > //注册失败
   > {'status': False, 'message': '用户已存在'}
   > ```

4. ##### ‘GetGroup/’

   > 功能：获取已存在信息组
   >
   > 请求方式：POST
   >
   > 请求表单form字段
   >
   > ```JSON
   > {
   > 	'SafetyCode':'登陆时服务器返回身份码'
   > }
   > ```
   >
   > 返回JSON格式数据
   >
   > 返回示例
   >
   > ```JSON
   > {
   >     'status': True, 
   >     'fieldNum': 3, 
   >     'Group': {
   >         'JG': '教改', 
   >         'JXCGJ': '教学成果奖', 
   >         'KCGG': '课程改革'
   >     }
   > }
   > ```

5. ##### ‘GetField/’

   > 功能：获取指定指定信息组所有字段名
   >
   > 请求方式：POST
   >
   > 请求表单form字段
   >
   > ```JSON
   > {
   > 	'SafetyCode':'登陆时服务器返回身份码',
   > 	'GroupName':'信息组名',
   > }
   > ```
   >
   > 返回JSON格式数据
   >
   > 返回示例
   >
   > ```JSON
   > {
   >     'status': True, 
   >     'Field': {
   >         'Object': '项目名', 
   >         'Person_Charge': '负责人', 
   >         'Person_Build': '立项参与人员', 
   >         'Person_Finish': '结题参与人员', 
   >         'College': '学院', 
   >         'Time_Build': '立项时间', 
   >         'Time_Finish': '结题时间', 
   >         'Object_Status': '项目状态', 
   >         'Object_Kinds': '项目种类'
   >     }
   > }
   > ```
   >
   > 

6. ##### ‘GetList/’

   > 功能：获取指定指定信息组指定字段所有信息
   >
   > 请求方式：POST
   >
   > 请求表单form字段
   >
   > ```JSON
   > {
   > 	'SafetyCode':'登陆时服务器返回身份码',
   > 	'GroupName':'信息组名',
   > 	'FiledName':'字段名',
   > 	'key':'约束字段名',
   > 	'value':'约束值',
   > }
   > ```
   >
   > 返回JSON格式数据
   >
   > 返回示例
   >
   > ```JSON
   > {
   > 	'status': True, 
   > 	'MessageNum': 219, 
   > 	'result': ['以行业工程实践应用型人才素质内涵为导向，着力进行轮机动力专业大类人才培养模				式改革', 
   >                '加强教学实践环节，培养卓越土木工程应用型人才'
   >               ]
   > }
   > ```

5. ##### ’GetLine/‘

   > 功能：获取指定指定信息组指定字段的该行信息
   >
   > 请求方式：POST
   >
   > 请求表单form字段
   >
   > ```JSON
   > {
   > 	'SafetyCode':'登陆时服务器返回身份码',
   > 	'GroupName':'信息组名',
   >     //不建议约束键值为空字符串，会导致返回该信息组所有条目信息
   > 	'key':'约束字段名',
   > 	'value':'约束值',
   > }
   > ```
   >
   > 返回JSON格式数据
   >
   > 返回示例
   >
   > ```JSON
   > {
   >     'status': True, 
   >     'MessageNum': 2, 
   >     'lines': {
   >         '0': {
   >             '项目名': '基于CDIO理念的经管类专业实践环节教学模式创新研究', 
   >             '负责人': '田剑', 
   >             '立项参与人员': ['王利', '姚慧丽', '吕向阳', '明洁'], 
   >             '结题参与人员': 'None', 
   >             '学院': '经济管理学院', 
   >             '立项时间': '2011-12', 
   >             '结题时间': 'None', 
   >             '项目状态': '放弃', 
   >             '项目种类': '重点'
   >         }
   >     }
   > }
   > ```

8. ##### ‘GetGroup/’

   > 功能：获取所有已存在信息组表明与字段名对照字典
   >
   > 请求方式：POST
   >
   > 请求表单form字段
   >
   > ```JSON
   > {
   > 	'SafetyCode':'登陆时服务器返回身份码',
   > }
   > ```
   >
   > 返回JSON格式数据
   >
   > 返回示例
   >
   > ```json
   > {
   >     'status': True,
   >     'fieldNum': 4,
   >     'Group': {
   >         'JG': '教改',
   >         'JXCGJ': '教学成果奖',
   >         'KCGG': '课程改革',
   >         'd4f3753ad439b0dabfda1f63efabf35a': 'A'
   >     }
   > }
   > ```

9. ##### ‘GetField/’

   > 功能：获取某个表名所有字段名对照
   >
   > 请求方式：POST
   >
   > 请求表单form字段

   > ```JSON
   > {
   > 	'SafetyCode':'登陆时服务器返回身份码',
   >     'GroupName':'指定信息组表名'
   > }
   > ```
   >
   > 返回JSON格式数据
   >
   > 返回示例
   >
   > ```json
   > {
   >     'status': True,
   >     'Field': {
   >         'ID': '序号',
   >         'Object': '项目名',
   >         'Person_Charge': '负责人',
   >         'Person_Build': '立项参与人员',
   >         'Person_Finish': '结题参与人员',
   >         'College': '学院',
   >         'Time_Build': '立项时间',
   >         'Time_Finish': '结题时间',
   >         'Object_Status': '项目状态',
   >         'Object_Kinds': '项目种类'
   >     }
   > }
   > ```

10. ##### ‘GlobalSearch/’

    > 功能：全局搜索
    >
    > 请求方式：POST
    >
    > 请求表单form字段
    >
    > ```JSON
    > {
    > 	'SafetyCode':'登陆时服务器返回身份码',
    >     'value':'搜索的关键字'
    > }
    > ```
    >
    > 返回JSON格式数据
    >
    > 返回示例
    >
    > ```JSON
    > {
    >     'status': True, 
    >     'result': {
    >         '关键词': '温大勇', 
    >         'listName': '关键词;搜索数目;Group',
    >         'Group': {
    >             '教改<1>': {
    >                 '60': '形势与政策课研究型交往式教学方法的探索'
    >             }, 
    >             '教学成果奖<1>': {
    >                 '73': '以“计算思维”为导向的计算机类专业创新型人才培养模式的改革与实践'
    >             }, 
    >             '课程改革<0>': {}, 
    >             'A<0>': {}
    >         }, 
    >         '搜索数目': 2
    >     }, 
    >     'allResult': {
    >         '教改<1>': [
    >             [60, '形势与政策课研究型交往式教学方法的探索', '周露平', '于立东 王军 赵敏 王瑜 郭红明 唐亮 温大勇', None, '苏州理工学院', '2011-12', None, '已结题', '一般']
    >         ], 
    >         '教学成果奖<1>': [
    >             [73, '以“计算思维”为导向的计算机类专业创新型人才培养模式的改革与实践', '段先华、潘 磊、张 静、程 科、张 明、景国良、温大勇、李永忠、吴 陈、徐 丹', '计算机科学与工程学院', '二等奖', '2016', '校级']
    >         ], 
    >         '课程改革<0>': [], 
    >         'A<0>': []
    >     }
    > }
    > ```

11. ‘GetFieldYX/’

    > 功能：获取指定信息组字段与中文对照表
    >
    > 请求方式：POST
    >
    > 请求表单form字段
    >
    > ```JSON
    > {
    > 	'SafetyCode':'登陆时服务器返回身份码',
    >     'GroupName':'指定信息组表名'
    > }
    > ```
    >
    > 返回JSON格式数据
    >
    > 返回示例
    >
    > ```JSON
    > {
    >     'status': True,
    >     'Field': {
    >         'EN': 'ID;Object;Person_Charge;Person_Build;Person_Finish;College;Time_Build;Time_Finish;Object_Status;Object_Kinds',
    >         'CN':'序号;项目名;负责人;立项参与人员;结题参与人员;学院;立项时间;结题时间;项目状态;项目种类'
    >     }
    > }
    > ```
    >
    > 

