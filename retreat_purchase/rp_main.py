# 爬取东方财富的打新数据
# http://data.eastmoney.com/xg/xg/default.html
import requests
from urllib.parse import unquote
import json
import pandas as pd
import time
# 英文-中文对照
columns={
    'securityshortname':'公司名称',
    'securitycode':'股票代码',
    'applyontMoney':'顶格申购金额',
    'issueprice': '发行价格',
    'newPrice': '收盘价',
    'lwr':'网上中签率',
    'mzyqhl':'一签获利',
    'listingdate':'上市日期'
}

url = 'http://dcfm.eastmoney.com/EM_MutiSvcExpandInterface/api/js/get'
data = {
    'callback': 'jQuery112307888979807342311_1620441095511',
    'st': 'purchasedate,securitycode',
    'sr': -1,
    'ps': 50,
    'p': 1,
    'type': 'XGSG_LB',
    'js': '{"data":(x),"pages":(tp)}',
    'token': '894050c76af8597a853f5b408b759f5d'
    }
requests.DEFAULT_RETRIES = 5  # 增加重试连接次数
s = requests.session()
s.keep_alive = False  # 关闭多余连接
response = requests.get(url, params=data)
response.encoding = 'utf_8'
content = unquote(response.text)

# 解析数据
sub_str = data['callback']
content = content[content.find(sub_str)+len(sub_str)+1:-1]
jjs = json.loads(content)

# 读取所有数据
pages = jjs['pages']
df = pd.DataFrame()
for p in range(pages):
    data['p'] = p+1
    resp = requests.get(url, params=data)
    resp.encoding = 'utf_8'
    c = unquote(resp.text)
    c = c[c.find(sub_str) + len(sub_str) + 1:-1]
    jj = json.loads(c)
    df = df.append(pd.DataFrame(jj['data']))
    print('完成 {0}.'.format(p+1))
    time.sleep(5)

# 排除部分数据
df = df.reset_index(drop=True)
df = df[(df['newPrice'] != '-') | (df['mzyqhl'] != '-')]
df['listingdate'] = df['listingdate'].apply(lambda x:str(x).split('T')[0])
# 选取需要的数据
df_short = df[columns.keys()].copy()
# 计算期望
df_short['inc'] = df_short['lwr'].astype('float') * df_short['mzyqhl'].astype('float')

df_short.sort_values(by='listingdate', ascending=False, inplace=True)
df_short = df_short.rename(columns=columns)
df_short.to_csv('result/all_new_stock.csv',index=False, encoding='utf_8_sig')
