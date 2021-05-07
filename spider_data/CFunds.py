import pandas as pd
import json
import requests
import time
from bs4 import BeautifulSoup

class ClosedFunds:
    """
    集思录上封闭型基金接口返回的数据
    https://www.jisilu.cn/data/cf/cf_list/?___jsl=LST___t=1620368194071
    """
    class Funds:
        """
        封闭型基金的属性
        """
        """
        {
            page: 1,
            total: '',
            rows:
            {
                id:'XXX', 
                cell:
                {
                    fund_id: "160526",
                    fund_nm: "博时优势",
                    pinyin: "bsys",
                    report_dt_: "2020-12-31",
                    report_nm: "2020年报",
                    maturity_dt: "2022-06-03",
                    open_maturity_dt: null,
                    fund_company: "博时基金",
                    amount_outstanding: null,
                    trade_amount: null,
                    issue_dt: "2019-06-03",
                    list_dt: "2019-12-02",
                    duration: 36,
                    status_cd: "N",
                    type_cd: "F",
                    open_dt: null,
                    ms_rating_3: null,
                    ms_rating_5: null,
                    ms_rating_10: null,
                    style: "灵活配置型",
                    company_hold: null,
                    notes: "封闭3年转LOF",
                    urls: "http://www.bosera.com/fund/160526.html",
                    ex_dt: null,
                    ex_info: null,
                    last_time: "14:16:00",
                    last_dt: "2021-05-07",
                    price: "1.3380",
                    increase_rt: "0.68",
                    volume: "12.68",
                    net_value: "1.4367",
                    nav_dt: "2021-05-06",
                    realtime_estimate_value: "1.4265",
                    realtime_estimate_dt: "2021-05-07 14:16:40",
                    discount_rt: "6.207",
                    left_year: "1.07",
                    annualize_dscnt_rt: "5.780",
                    quote_incr_rt: "0.53",
                    nav_incr_rt: "-0.39",
                    spread: "-0.91",
                    stock_ratio: "91.20",
                    report_dt: "2021-03-31",
                    daily_nav_incr_rt: "-0.71",
                    daily_spread: "-1.39",
                    owned: 0,
                    maturity_dt_show: "2022-06-03"
                }
            }
        }
        """
        def __init__(self, entries):
            # 基金代码
            self.fund_id = None
            # 基金名称
            self.fund_nm = None
            # 基金拼音
            self.pinyin = None
            # 上次报告时间？
            self.report_dt_ = None
            # 报告名称
            self.report_nm = None
            # 到期时间
            self.maturity_dt = None
            # 转换开基时间？
            self.open_maturity_dt = None
            # 基金公司名称
            self.fund_company = None
            # 未付金额？
            self.amount_outstanding = None
            # 交易数量？
            self.trade_amount = None
            # 发行时间
            self.issue_dt = None
            # 首次公布时间？
            self.list_dt = None
            # 历时多久 (月)
            self.duration = None
            # ？
            self.status_cd = None
            # 标识是否封闭式
            self.open_dt = None
            self.ms_rating_3 = None
            self.ms_rating_5 = None
            self.ms_rating_10 = None
            # 基金分类
            self.style = None
            # 担保公司
            self.company_hold = None
            # 备注
            self.notes = None
            # 基金详细网址
            self.urls = None
            self.ex_dt = None
            self.ex_info = None
            self.last_time = None
            self.last_dt = None
            # 现价
            self.price = None
            # 涨幅
            self.increase_rt = None
            # 成交金额
            self.volume = None
            # 净值
            self.net_value = None
            # 净值日期
            self.nav_dt = None
            # 最近估值
            self.realtime_estimate_value = None
            # 最近估值时间
            self.realtime_estimate_dt = None
            # 折价率
            self.discount_rt = None
            # 剩余年限
            self.left_year = None
            # 年化折价率
            self.annualize_dscnt_rt = None
            # 周价增
            self.quote_incr_rt = None
            # 周净增
            self.nav_incr_rt = None
            # 近1个周净增 天天基金网
            self.week1_nav_incr_rt = None
            # 近1个月净增 天天基金网
            self.month1_nav_incr_rt = None
            # 净价差
            self.spread = None
            # 股票配置比
            self.stock_ratio = None
            # 最近一次报告时间
            self.report_dt = None
            # 日净增
            self.daily_nav_incr_rt = None
            # 日净差
            self.daily_spread = None

            self.owned = None
            # 到期时间
            self.maturity_dt = None
            self.maturity_dt_show = None

            self.__dict__.update(entries)

    @staticmethod
    def get_nac_ttjj(code):
        """
        从天天基金网获取 基金的近一个月,一个周的月净增
        :param code: 基金代码
        :return:
        """
        ttjj_address = 'http://fund.eastmoney.com/{0}.html'.format(code)
        response = requests.get(ttjj_address)
        response.encoding = 'utf-8'
        content = response.text
        if content is not None or content!='':
            bs = BeautifulSoup(response.text, features='html.parser')

            li = bs.find('li', id='increaseAmount_stage', attrs={'class': 'increaseAmount'})
            tds = li.table.find_all('tr')[1].find_all('td')
            week_nav = tds[1].div.text
            month_nav = tds[2].div.text
            return week_nav, month_nav
        else:
            return 0, 0
    def update(self):
        timestamp = int(time.time() * 1000)
        jsl_address = 'https://www.jisilu.cn/data/cf/cf_list/?___jsl=LST___t={0}'.format(timestamp)
        response = requests.get(jsl_address)
        all_content = json.loads(response.text)
        self.page = all_content['page']
        self.funds = []
        cfs = []
        for r in all_content['rows']:
            info = r['cell']
            fund = self.Funds(info)
            fund.week1_nav_incr_rt, fund.month1_nav_incr_rt = \
                self.get_nac_ttjj(fund.fund_id)
            self.funds.append(fund)
            info['week1_nav_incr_rt'] = fund.week1_nav_incr_rt
            info['month1_nav_incr_rt'] = fund.month1_nav_incr_rt
            cfs.append(info)
        self._dict = all_content
        # all_df 为所有的封基数据
        self.all_df = pd.DataFrame(cfs)

    def __init__(self):
        self.page = None
        self.total = None
        self.funds = None
        self._dict = None
        self.all_df = None
        # 获取最新数据
        self.update()

    def get_cf(self):
        """
        返回所有封闭式基金
        :return:
        """
        return self.all_df
