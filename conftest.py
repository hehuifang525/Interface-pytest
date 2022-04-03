import pytest

from base.common import mysql, es


@pytest.fixture(scope="session", autouse=True)
def disconnect():
    """
    结束脚本时的操作
    """
    yield
    mysql.conn.close()  # 关闭数据库连接
    es.close()  # 关闭es连接
    print("已关闭数据库和es连接")


def pytest_collection_modifyitems(items):
    """
    测试用例收集完成时，将收集到的item的name和nodeid的中文显示在控制台上
    :return:
    """
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")
