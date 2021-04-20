import requests
import time
from CBont import ConvertibleBond
import json

# jisilu 可转债
timestamp = int(time.time()*1000)
jsl_address = 'https://www.jisilu.cn/data/cbnew/cb_list/?___jsl=LST___t={0}'.format(timestamp)

response = requests.get(jsl_address)
all_content = json.loads(response.text)
cb = ConvertibleBond(all_content)

# 获取可转债
ccb = cb.get_cb(cb_type='C')

# 按照价格从小到大排序
ccb1 = ccb['price'].astype('float').sort_values().values



