import pymysql
import configparser


class Mysql:
    """
    专用于数据库连接的class
    """
    def __init__(self):
        conf = configparser.ConfigParser()
        conf.read("config.ini")
        self.conn = pymysql.connect(
            host=conf.get('ServiceCool', 'mysql_host'),
            port=int(conf.get('ServiceCool', 'mysql_port')),
            user=conf.get('ServiceCool', 'mysql_user'),
            passwd=conf.get('ServiceCool', 'mysql_password'),
            db=conf.get('ServiceCool', 'mysql_db'))

    def cursor_conn(self, statement):
        """
        传入sql执行语句并返回所有结果
        """
        cursor = self.conn.cursor()
        cursor.execute(statement)
        result = cursor.fetchall()
        cursor.close()
        self.conn.commit()
        return result

    def get_value(self, table: str, key, field: str, field_value, field_str=""):
        """
        查询table表中，field值为field_value的数据的key的值
        """
        if field_str != "":
            statement = "SELECT %s FROM %s WHERE %s" % (key, table, field_str)
        else:
            statement = "SELECT %s FROM %s WHERE %s='%s'" % (key, table, field, field_value)
        result = self.cursor_conn(statement)
        return result

    def get_max(self, table: str, key):
        """
        查询table表中，field值的最大值
        """
        statement = "SELECT MAX(%s) FROM %s" % (key, table)
        result = self.cursor_conn(statement)
        return result[0][0]

    def get_min(self, table: str, key):
        """
        查询table表中，field值的最大值
        """
        statement = "SELECT MIN(%s) FROM %s" % (key, table)
        result = self.cursor_conn(statement)
        return result[0][0]
