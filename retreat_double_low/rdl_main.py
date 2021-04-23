import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

his_data = pd.read_table('history_data.txt', header=None,
                         encoding='utf-8',delim_whitespace=True)
his_data.rename(columns={0:'date',1:'name',2:'pr',3:'price',4:'back'},inplace=True)
vc=his_data['date'].value_counts()
"""
查看转债数量分布情况
sns.barplot(x=vc.index,y=vc.values)
plt.show()
"""
"""
转债个数|双低数量
20~50|5
50~100|8
100~200|15
200~|20
"""
his_data['db_low'] = his_data['price']+his_data['pr']
day_20_50 = vc[(vc>20) & (vc<=50)].index.values
day_50_100 = vc[(vc>50) & (vc<=100)].index.values
day_100_200 = vc[(vc>100) & (vc<=200)].index.values
day_200_now = vc[vc>200].index.values
nums_dict = {
    'lt_20':0,
    '20_50':5,
    '50_100':8,
    '100_200':10,
    '200_now':15
}


# 根据目前可转债数量决定双低转债轮动数量
def get_number(size, dict):
    if size <= 20:
        return dict['lt_20']
    elif 20 < size <= 50:
        return dict['20_50']
    elif 50< size<=100:
        return dict['50_100']
    elif 100<size <=200:
        return dict['100_200']
    else:
        return dict['200_now']

# 间隔天数 1代表操作隔一天
space_day = 1
# 净值为1
net_value = 1
# 目前持有股票
holding_stocks=[]
#
day_ = vc.sort_index()
day_index = np.sort(vc.index.values)
# 买入记录
buy_records = []
# 卖出记录
sell_records=[]
# 净值记录
net_values=[]
for i in range(day_index.size):
    today = day_index[i]
    today_data = his_data[his_data['date']==today].copy()
    num_ = get_number(today_data.shape[0], nums_dict)
    if num_==0:
        # 如果轮动数量为0 说明可转债数量低于20 没有轮动意义
        print('低于20,跳过{0}.'.format(today))
        continue
    rate = 1 / num_
    if (i+1)%space_day == 0:
        # 当天交易
        # 净值初始化
        nv = 0
        if holding_stocks is not None and len(holding_stocks) != 0:
            # 首先将上期的持有股票卖掉
            for stock_info in holding_stocks:
                stock_name = stock_info['name']
                ttdv = today_data.loc[today_data['name'] == stock_name, 'price'].values
                # 判断是否当前债券可能强赎
                sell_price = float(stock_info['price'] if len(ttdv)==0 else ttdv[0])
                stock_buy_price = stock_info['price']
                nv = nv + sell_price/stock_buy_price*rate
                sell_records.append({
                    'name': stock_name,
                    'date': today,
                    'sell_price': sell_price,
                    'buy_price': stock_buy_price
                })
        else:
            # 如果没有持仓，不用操作
            pass
        # 然后计算当日双低前n进行买入并记录
        today_data.sort_values(by='db_low',inplace=True)
        topN = today_data.head(num_)
        for j in range(num_):
            tj = topN.iloc[j]
            # 购买记录
            sell_records.append({
                'name':tj['name'],
                'date': today,
                'buy_price': tj['price']
            })
            # 添加到持仓
            holding_stocks.append({
                'name': tj['name'],
                'price': tj['price']
            })
    else:
        # 不交易 波动为1 即不变
        nv = 1
    print("第{0}个数据的时间为{1}".format(i,today))
    net_value = net_value*nv
    net_values.append(net_value)
