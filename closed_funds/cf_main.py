from spider_data.CFunds import ClosedFunds
import pandas as pd
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', None)
pd.set_option("display.max_colwidth", 100)
cf = ClosedFunds()
df = cf.get_cf()
df['week1_nav_incr_rt'] = df['week1_nav_incr_rt'].str.strip('%').astype('float')
df['month1_nav_incr_rt'] = df['month1_nav_incr_rt'].str.strip('%').astype('float')
# 权重比例 weight 周和月比例设置 1：4
weight = 4
# 目前综合得分按照  week+month/4 计算
df['score'] = df['week1_nav_incr_rt'] + df['month1_nav_incr_rt']/weight
df['score'] = df['score'].apply(lambda x: round(x,2))
columns = {'fund_id': '基金代码',
           'fund_nm': '基金名称',
           'fund_company': '基金公司',
           'maturity_dt': '到期时间',
           'discount_rt': '折价率',
           'left_year': '剩余时间',
           'week1_nav_incr_rt': '每周增幅',
           'month1_nav_incr_rt': '每月增幅',
           'score': '综合得分'}
df_score = df[columns.keys()].sort_values(by='score', ascending=False)
df_score = df_score.rename(columns=columns)
file_name = 'result/cf_1_{0}.csv'.format(weight)
df_score.to_csv(file_name, index=False, encoding='utf_8_sig')

