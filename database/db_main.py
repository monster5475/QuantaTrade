import sqlite3
from config import Config


file_name = 'test.db'
file_path = Config.get_data_dir() + file_name
conn = sqlite3.connect(file_path)
cursor = conn.cursor()

sql = 'create table students(id int primary key, name varchar(20) not null , age int not null)'
cursor.execute(sql)  # 创建表的命令

cursor.close()
conn.close()



# sql = 'insert into port values(?,?)'
# cursor.execute(sql,['114.114.114.114',65535])
# conn.commit()
#
# cursor.execute('select * from port')
# print(cursor.fetchall())