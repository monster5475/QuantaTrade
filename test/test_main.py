from database.action.crud import Sqlite3Action
import sqlite3
from database.config import Config

Sqlite3Action.init_conn(db_name='test')
sql = 'select * from students'
res = Sqlite3Action.execute(db_name='test', sql=sql)
Sqlite3Action.close(db_name='test')
print(res)
