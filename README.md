## 环境依赖
python 3.7+

pytest	6.2.4

pytest-rerunfailures	10.1	

allure-pytest	2.9.43

pytest-ordering	0.6	0.6

allure的安装详见 https://www.cnblogs.com/yoyoketang/p/12004145.html

## 文件命名规则

```shell
sc-pytest                  //项目名
├── api_testcases               //接口测试用例文件夹        
│    ├── web_user               //web端服务人员界面
│          ├──ticket            //工单模块
│               ├──ticket_create_a                      //此模块的所有Action
│               │   ├──StoreNew                         //此Action下的所有subaction
│               │        ├──__init__.py                 //必要
│               │        ├──test_cases.py               //接口测试例集
│               │        ├──fuction.py                  //接口函数
│               ├──__init__.py                          //必要
│               ├──test_cases.py                        //工单场景测试例
│          ├──action_re_body.py                         //通用请求body,勿动
│          ├──conftest.py                               //web_user的前置后置函数及钩子函数文件
├── base                        //基础文件
│    ├── common.py              //通用函数
│    ├── Mysql.py               //mysql相关函数
│    ├── format_json.html       //请求的返回基础格式,勿动
├── conftest.py                 //总体前置后置函数及钩子函数文件
├── debug_test.py               //本地调试文件
├── main.py                     //jenkins执行文件,勿动

```


## 规范
1.每个函数都要添加注释，在方法名下方编写
```shell
def test_fail2_check(TicketID, message):
    """
    rd工单2020111210000034版本-查看工单详情接口-查看错误工单

    :param TicketID:工单ID
    :param message: 报错信息
    :return: 字段的FormID
    """
```
2.每个断言（assert）都要写注释
```shell
    assert status_code == 200, "请求状态码"
    assert result == 1, "接口状态码"
```
3.用例的执行顺序规定（@pytest.mark.run(order=3)）
```
① 初始化类用例order为1-10：初始化检查类为1，初始化创建为2及之后
② 普通类用例为11之后，也可以不填写
③ 前后置函数写在conftest.py里，使用方法见知识点2.
```


## 执行命令

#### `jenkins` 执行：
```
python main.py --url_host 接口的host --url_user 接口登录名 --url_password 接口密码 --mysql_host 数据库ip --mysql_port 端口 --mysql_user root 数据库用户名 --mysql_password 数据库密码 --mysql_db 数据库名称 --test_path 需要执行的文件的路径（绝对路径或相对路径）
```
示例：
```
python main.py --url_host http://auto-test.k8s.devops:31080 --url_user root@localhost --url_password 123456 --mysql_host 192.168.123.195 --mysql_port 3306 --mysql_user root --mysql_password 123456 --mysql_db auto_test --test_path testsuites
```

#### `debug文件` 执行 `推荐`：
```
  debug_test.py文件里pytest.main函数的第二个参数为[用例文件夹相对路径]，后面的参数为报告相关参数，可不动
  若有其他插件参数可往后添加
  若需要执行单个测试用例，可以把路径后加上::用例名，例api_testcases/web_user/ticket_template/test_cases.py::test_SC_Template_31
```
示例：
```
if __name__ == '__main__':
    pytest.main(["-vs", "api_testcases", '--alluredir', './report_temp', '--clean-alluredir'])
    os.system('allure serve ./report_temp')
```


#### `命令行` 执行：
```
pytest [pytest执行参数][用例文件夹相对路径] [插件参数]
```
示例：
```
pytest -vs api_testcases --alluredir ./report_temp --clean-alluredir
```

## 知识点

1.报告优先级标记（@allure.severity('XXX')）
```
Blocker级别：中断缺陷（客户端程序无响应，无法执行下一步操作）
Critical级别：临界缺陷（ 功能点缺失）
Normal级别：普通缺陷（数值计算错误）
Minor级别：次要缺陷（界面错误与UI需求不符）
Trivial级别：轻微缺陷（必输项无提示，或者提示不规范）
```
2.conftest.py前后置函数的使用 @pytest.fixture(scope="module", autouse=True)进行标记。
`scope`为执行频率
```
function：默认范围，每一个函数或方法都会调用，不填写时便是它
class：每一个类调用一次
module: 每一个.py文件调用一次，文件中可以有多个function和class
session：多个文件调用一次，可以跨文件，如在.py文件中，每一个.py文件就是module
范围：
session > module > class > function
```
`autouse=True`表示给每个用例加上该前后置函数，使用时得注意scope的标注

3.py文件的import调用

调用`同一个文件夹或子文件夹内`的文件可以用相对路径，例from .api import *

调用`别的文件夹内`的文件`必须`用绝对路径，例from api_testcases.web_user.action_re_body import *

4.用例的标注方式有两种：

①用ids数列进行标注，例
```
@pytest.mark.parametrize("TicketID", [0,1,2], ids=["工单ID为0","工单ID为1","工单ID为2"])
```
②用pytest.param实例一个参数组，例
```
@pytest.mark.parametrize('FieldType', [pytest.param('Date', id='日期（年月日）'),
                                       pytest.param('DateTime', id='日期'),
                                       pytest.param('Text', id='文本'),
                                       pytest.param('TextArea', id='多文本')])
```

## 参数化

在每个test_cases.py中的每个用例头部用标注进行编写，一共有三种方式：
1.直接指定参数列表、2.引用自定义函数、3.把函数当做参数


1.直接指定参数列表：

```
单个参数示例:
    @pytest.mark.parametrize("user_id", [1001, 1002, 1003, 1004])
    def test_XXX(user_id):
        pass
多个参数示例：
    @pytest.mark.parametrize("user_id,pwd", [(1001,1), (1002,2), (1003,3)])
    def test_XXX(user_id, pwd):
        pass
```

2.引用自定义函数：可直接调用debugtalk中的自定义函数，但函数必须有返回：

```
单个参数可直接返回一个list或元素为字典的list，例 [{"user_id": 1001}, {"user_id": 1002}, {"user_id": 1003},]
多个参数示例得返回一个内嵌的list，例 [["user1", "111111"],["user2", "222222"],["user3", "333333"]]
或返回一个元素为字典的list，例：[{"user_id": 1001,"password":"111111"}, {"user_id": 1002,"password":"222222"}, {"user_id": 1003,"password":"333333"},]
```

3.把函数当做参数（常用于接口依赖）

通过indirect=True把login当作函数去执行，login后的test_user_data为login的参数化，login本身必须有return
```
@pytest.mark.parametrize('login',test_user_data,indirect=True)
def test_cart(login):
```

用例执行次数根据parameters中列举的每行参数组合的用例数量的笛卡尔积决定。
例：
```
@pytest.mark.parametrize('user_agent', ["iOS/10.1", "iOS/10.2", "iOS/10.3"])
@pytest.mark.parametrize('app_version',app_version())
@pytest.mark.parametrize('os_platform',get_os_platform())
```
其中app_version()有两条数据，get_os_platform()返回的list有四个元素，那么执行的组合为3*2*4，即该接口将运行24次。

## 录制并生成测试用例
1.打开chrome浏览器，按下F12按钮，选择名为Network的tab，观察页面请求情况

![名为Network的tab](https://git.otrs365.cn/testdepartment/sc-pytest/raw/master/base/image/Network.png)

2.在对应的页面上进行操作

3.生成单个接口测试用例：
```
在F12窗口上点击对应的请求，按下鼠标右键，选择Copy-Copy as fetch
```

![Copy as fetch](https://git.otrs365.cn/testdepartment/sc-pytest/raw/master/base/image/Copy_as_fetch.png)

生成多个接口测试用例
```
在F12窗口上点击任意的请求，按下鼠标右键，选择Copy-Copy all as fetch

注：该操作会复制当下F12窗口里记录的所有请求
```

![Copy all as fetch](https://git.otrs365.cn/testdepartment/sc-pytest/raw/master/base/image/Copy_all_as_fetch.png)

4.把复制的内容粘贴至项目base文件夹下的request_copy文件中

![request_copy文件](https://git.otrs365.cn/testdepartment/sc-pytest/raw/master/base/image/request_copy.png)

5.运行项目根目录下的auto_create.py脚本

![auto_create.py脚本](https://git.otrs365.cn/testdepartment/sc-pytest/raw/master/base/image/auto_create.png)

注：
```
①若是老式含Action和Subaction的请求，则会对应生成至web_user或web_customer文件夹下，并按照Action和Subaction生成相应的文件夹。
 可直接把生成的文件复制至对应模块的文件夹内；
②若是其他请求，则会对应在根目录下生成test_cases文件夹。可进行更改后移至对应路径。
```