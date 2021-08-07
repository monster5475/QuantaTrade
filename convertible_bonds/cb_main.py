# 抓妖债，主要是15只，首先获取可转债溢价率中位数，向下选择规模在4亿以下
from spider_data.CBont import ConvertibleBond

cb = ConvertibleBond()
ccb = cb.get_cb(cb_type='C')
ccb['curr_iss_amt'] = ccb['curr_iss_amt'].astype(float)
ccb['year_left'] = ccb['year_left'].astype(float)
# 筛选规模在4亿以下
ccb = ccb[ccb['curr_iss_amt'] < 4].copy()
# 剔除一年内到期
ccb1 = ccb[ccb['year_left']>1].copy()
ccb1['premium_rt'] = ccb1['premium_rt'].apply(lambda x: float(x[:-1]))
half_number = int(ccb1.shape[0]/2)
# 获取溢价率中位数以下
ccb_half = ccb1.sort_values(by='premium_rt', ascending=False).iloc[half_number:]

cn_columns = {
    'bond_id': 'id',
    'bond_nm': '名称',
    'premium_rt': '溢价率',
    'curr_iss_amt': '剩余规模',
    'orig_iss_amt': '原始规模',
    'dblow': '双低价格',
    'year_left': '剩余时间'
}
ccb_dest = ccb_half[cn_columns.keys()].rename(columns=cn_columns)
print(' '.join(ccb_dest[:20]['id']))