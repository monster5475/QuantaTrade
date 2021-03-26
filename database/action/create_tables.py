import sqlite3
import os
from database.config import Config


def create_new():
    """
    创建双低记录的三个表
    :return:
    """
    file_name = 'double_low.db'
    file_path = Config.get_data_file_path(file_name)
    # 如果存在就删除
    if os.path.exists(file_path):
        os.remove(file_path)
    conn = sqlite3.connect(file_path)
    cursor = conn.cursor()
    # 创建现金记录表
    sql1 = 'create table cash_record(id integer primary key autoincrement, time date,' \
          'action_record_id int not null, last_cash float not null, now_cash float not null)'

    # 创建下单记录表
    sql2 = 'create table action_record(id integer primary key autoincrement, time date,' \
           'name varchar (50) not null, code varchar (10) not null, number int not null, price float not null,' \
           'type varchar (10) not null)'

    # 创建持仓表
    sql3 = 'create table stock(id integer primary key autoincrement, name varchar (50) not null, ' \
           'code varchar (10) not null, number int not null, buy_number int not null, ' \
           'sell_number int not null )'
    cursor.execute(sql1)
    cursor.execute(sql2)
    cursor.execute(sql3)
    conn.commit()
    cursor.close()
    conn.close()