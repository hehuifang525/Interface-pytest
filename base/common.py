# coding:utf-8
import base64
import configparser
import datetime
import json
import ntpath
import re
import string
import time
import random
from urllib import parse
from elasticsearch import Elasticsearch
import allure
import requests
from bs4 import BeautifulSoup

from base.Mysql import Mysql

conf = configparser.ConfigParser()
conf.read('config.ini')
mysql = Mysql()

es = Elasticsearch(host="analysis-ik.k8s.devops", port=31080)


# pytest相关----------------------------
@allure.step("发送请求")
def send_request(method, url, headers='', data='', params='', file_path=None):
    """
    请求封装，并把返回的json呈折叠展示在报告中

    :param method: eg.POST/GET 请求方法
    :param url: 请求路径
    :param headers: 请求头
    :param data: 请求体
    :param params: 参数体
    :param file_path: 请求附件路径
    """
    if file_path:
        files = {'Files': (ntpath.basename(file_path), open(file_path, 'rb'))}
        result = requests.request(method, url, headers=headers, params=params, files=files)
        allure.attach.file(file_path, '附件')
    else:
        result = requests.request(method, url, headers=headers, data=data)
    req_text = BeautifulSoup(open('base/format_json.html', encoding='utf-8'), 'html.parser')
    textarea = req_text.find('textarea', id="json-input")
    textarea.string = json.dumps(result.json(), ensure_ascii=False, indent=4)
    allure.attach(req_text.prettify(), '响应', allure.attachment_type.HTML)
    return result


@allure.step("正向请求返回的固定校验")
def success_assert(status_code, result):
    """
    正向请求返回的固定校验

    :param status_code: eg:result.status_code 返回的状态码，200表示请求连接正常
    :param result: 请求自带的状态码
    """
    assert status_code == 200, "请求状态码"
    assert result == 1, "接口状态码"


@allure.step("负向请求返回的固定校验")
def fail_assert(status_code, re_json, message):
    """
    负向请求返回的固定校验

    :param status_code: eg:result.status_code 返回的状态码，200表示请求连接正常
    :param re_json: eg.result.json() 返回的内容
    :param message: 期望的报错提示信息
    """
    assert status_code == 200, "请求状态码"
    assert re_json['result'] == 0, "接口状态码"
    assert re_json['data']['message'] == message, "接口信息"


# config相关----------------------------
def config_read(section: str, key: str):
    """
    返回config文件对应section中key的值
    """
    return conf.get(section, key)


def config_write(section: str, key: str, value: str):
    """
    给config文件对应section中的key赋予value值
    """
    conf.set(section, key, value)
    conf.write(open('config.ini', "w"))
    return 1


def config_write_random(section: str, key: str, value: str):
    """
    给config文件对应section中的key赋予value值,
    value的值是拼接了输入字符串和时间随机数
    """
    value = value + str(get_datetime())
    config_write(section, key, value)
    time.sleep(0.00001)
    return value


def config_get_list_value(section: str, key_list: list = []):
    """
    获取config文件中对应section中list内key的value值
    """
    re_list = []
    for i in key_list:
        re_list.append(conf.get(section, i))
    return re_list


def config_get_section_value(section: str, exclude: list = []):
    """
    获取config文件中对应section中除exclude中以外所有key的value值
    """
    key_list = conf.options(section)
    re_list = []
    for i in key_list:
        if i not in exclude:
            re_list.append(conf.get(section, i))
    return re_list


# mysql相关----------------------------
def mysql_close():
    """
    关闭数据库连接
    用于logout接口
    """
    mysql.conn.close()
    return 1


def mysql_get_value(table: str, key: str, field: str, field_value, field_str=""):
    """
    查询table表中，field值为field_value或搜索条件为field_str的数据的值
    """
    result = mysql.get_value(table, key, field, field_value, field_str)
    return mysql_format_trans(result)


def mysql_get_list(table: str, key: str, field: str, field_value, field_str=""):
    """
    查询table表中，field值为field_value或搜索条件为field_str的数据的所有值
    """
    result = mysql.get_value(table, key, field, field_value, field_str)
    return None if len(result) == 0 or result[0][0] is None else [x[0] for x in result]


def mysql_format_trans(result):
    """
    mysql结果格式转换
    """
    if len(result) == 0 or result[0][0] is None:
        return None
    elif type(result[0][0]) is bytes:
        return str(result[0][0], encoding="utf-8")
    return str(result[0][0])


def mysql_format_trans2(result):
    """
    mysql结果格式转换
    """
    if len(result) == 0 or result[0][0] is None:
        return ''
    elif type(result[0][0]) is bytes:
        return str(result[0][0], encoding="utf-8")
    return str(result[0][0])


# Elasticsearch相关----------------------------
def es_search_list(index, body, field):
    """
    Elasticsearch获取指定字段的列表
    """
    result = es.search(index=index, body=body)
    return None if 'hits' not in result['hits'] else [x['_source'][field] for x in result['hits']['hits']]


# 编码相关----------------------------
def base64_encode_all(dic: dict):
    """
    把dic中的key和value全部进行base64编码后再进行一次base64编码
    常用于新增接口
    """
    dic_re = {}
    for j in dic.keys():
        if type(dic[j]) is str:
            j_value = base64.b64encode(dic[j].encode()).decode()
        elif type(dic[j]) is list:
            j_value = []
            for i in dic[j]:
                j_value.append(base64.b64encode(i.encode()).decode())
        else:
            j_value = dic[j]
        j_key = base64.b64encode(j.encode()).decode()
        dic_re[j_key] = j_value
    json_re = json.dumps(dic_re)
    return base64.b64encode(json_re.encode()).decode()


def base64_encode_value(dic: dict):
    """
    把dic中的value进行base64编码后再进行一次base64编码
    常用于新增接口
    """
    dic_re = {}
    for j in dic.keys():
        if type(dic[j]) is str:
            j_value = base64.b64encode(dic[j].encode()).decode()
        elif type(dic[j]) is list:
            j_value = []
            for i in dic[j]:
                j_value.append(base64.b64encode(i.encode()).decode())
        else:
            j_value = dic[j]
        dic_re[j] = j_value
    json_re = json.dumps(dic_re)
    return base64.b64encode(json_re.encode()).decode()


def url_encode(data):
    """
    把data先进行一次url编码
    """
    return parse.quote(json.dumps(data))


# 其他----------------------------
def to_none_or_str(value):
    """
    判断value是否为空值，是则传入空值
    常用于csv参数化（csv无法传入空值）
    """
    return str(value) if value != 'None' else json.loads('null')


def get_datetime():
    """
    获取当前的日期（年月日时分秒微秒）
    """
    time.sleep(0.00001)
    return datetime.datetime.now().strftime('%y%m%d%H%M%S%f')


def check_response(_json, list_a):
    """
    递归遍历每一层的json，查找值是否存在
    """
    try:
        for list_key in _json:
            value = _json[list_key]
            if list_a[0] == value or list_a[0] == list_key:
                list_a.remove(list_a[0])
    except BaseException:
        for key_po in _json:
            if isinstance(_json[key_po], dict):
                check_response(_json[key_po], list_a)

    for key_po in _json:
        if isinstance(_json[key_po], dict):
            check_response(_json[key_po], list_a)
    return list_a


def get_result(_json, list_a):
    """
    判断值是否找到
    """
    list_pra = []
    list_pra.append(list_a)
    list_a = check_response(_json, list_pra)
    if len(list_a) == 0:
        return "匹配成功"
    else:
        return "匹配不成功"


def file_upload(filepath):
    """
    打开指定路径filepath的文件
    用于Content-Type为特殊值的文件上传接口
    """
    return open(filepath, "rb")


def get_file_name(filepath):
    """
    获取指定路径filepath的文件名
    """
    return ntpath.basename(filepath)


def get_32_random():
    """
    获取由[0-9，a-f]组成的32位随机数
    """
    token = string.ascii_lowercase[:6] + string.digits
    return ''.join(random.choice(token) for _ in range(32))


def get_moblie_number(moblie):
    """
    随机生成手机号，前三位数字作为参数传入
    """
    moblie_number = str(moblie) + str(random.randint(10000000, 99999999))
    return moblie_number


def get_regex_value(body, regex: str, var: str):
    """
    用得到的变量var替换正则表达式中的%%%，并执行正则表达式，获取body中的指定值
    """
    result = re.findall(regex.replace('%%%', var), json.dumps(body))
    return result[0]


def disorder_list_order(input_list):
    """
    随机打乱输入的列表排序
    """
    if type(input_list) is str:
        input_list = eval(input_list)
    random.shuffle(input_list)
    return str(input_list)


def list_superpose(inp):
    """
    叠加输入的列表
    """
    if type(inp) is str:
        inp = eval(inp)
    inp.extend(inp)
    return str(inp)
