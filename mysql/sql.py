import pymysql


class mysql():
    def __init__(self):
        pass

    """
    链接数据库
    """

    def connect_sql(self):
        """
        链接数据库，并返回游标
        :return: cursor游标、链接对象
        """
        # 连接mysql数据库
        con = pymysql.Connect(
            host="localhost",
            port=3306,
            user="root",
            password="root",
            db="homework",
            charset="utf8"
        )
        # 获取游标
        cursor = con.cursor()
        return con, cursor

    def close_sql(self, cursor):
        """
        关闭数据库
        :param cursor:
        :return:
        """
        cursor.close()
