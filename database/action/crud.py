import threading
import sqlite3
from database.config import Config


class Sqlite3Action:
    # 用来构建 连接池
    conn_dict = {}
    # 同步锁
    mutex = threading.Lock()

    def __init__(self):
        pass

    @classmethod
    def init_conn(cls, db_name):
        """
        首先拿到同步锁 然后获取连接 可能是新建 或者来自连接池
        :param db_name:
        :return:
        """
        try:
            cls.mutex.acquire()
            db_file_path = Config.get_data_file_path(db_name)
            if db_name in cls.conn_dict.keys():
                conn = cls.conn_dict[db_name]
            else:
                conn = sqlite3.connect(database=db_file_path)
                cls.conn_dict[db_name] = conn
        finally:
            cls.mutex.release()
        return conn

    @classmethod
    def close(cls, db_name):
        """
        删除db_name对应的连接
        :param db_name:
        :param connection
        :return:
        """
        try:
            cls.mutex.acquire()
            if db_name in cls.conn_dict.keys():
                cls.conn_dict[db_name].close()
                cls.conn_dict.pop(db_name)
        finally:
            cls.mutex.release()

    @classmethod
    def clear(cls):
        """
        清空所有的连接
        :return:
        """
        try:
            cls.mutex.acquire()
            for key in cls.conn_dict.keys():
                cls.conn_dict[key].close()
            cls.conn_dict.clear()
        finally:
            cls.mutex.release()

    @classmethod
    def execute(cls, db_name, sql, params=None):
        """
        执行语句
        :param db_name:
        :param sql:
        :param params:
        :return:
        """
        conn = cls.conn_dict[db_name]
        cursor = conn.cursor()
        results = None
        try:
            if '?' in sql:
                cursor.execute(sql, args=params)
            else:
                cursor.execute(sql)
            conn.commit()
            results = cursor.fetchall()
        except Exception as e:
            conn.rollback()
            print(e)
        cursor.close()
        return results
