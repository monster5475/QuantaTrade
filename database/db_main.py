import sqlite3
from config import Config
from database.action.crud import Sqlite3Action

conn = sqlite3.connect(Config.get_data_file_path('test'))
cursor= conn.cursor()
sql = 'select * from students'
cursor.execute(sql)
conn.commit()
res = cursor.fetchall()
print(res)
cursor.close()
conn.close()