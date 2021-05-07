import requests
import time
from CBont import ConvertibleBond
from CFunds import ClosedFunds
import json


def get_cb_jsl():
    # jisilu 可转债
    cb = ConvertibleBond()
    # 获取可转债
    ccb = cb.get_cb(cb_type='C')
    # 按照价格从小到大排序
    ccb1 = ccb['price'].astype('float').sort_values().values
    return ccb1

cf = ClosedFunds()
df = cf.get_cf()