import pandas as pd
import json
import requests
import time

class ConvertibleBond:
    """
    集思录可转债接口返回的数据 （包括可交换债）
    https://www.jisilu.cn/data/cbnew/cb_list/?___jsl=LST___t=1606138878882
    """
    class Bond:
        """
        集思录上可转债数据的属性
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
                    bond_id: "120004",
                    bond_nm: "20华菱EB",
                    stock_id: "sz000932",
                    stock_nm: "华菱钢铁",
                    btype: "E",
                    convert_price: "5.13",
                    convert_price_valid_from: null,
                    convert_dt: "2021-08-26",
                    maturity_dt: "2025-01-09",
                    next_put_dt: "2024-01-09",
                    put_dt: null,
                    put_notes: null,
                    put_price: "100.000",
                    put_inc_cpn_fl: "y",
                    put_convert_price_ratio: "43.42",
                    put_count_days: 30,
                    put_total_days: 30,
                    put_real_days: 0,
                    repo_discount_rt: "0.81",
                    repo_valid_from: "2021-04-12",
                    repo_valid_to: "2021-04-12",
                    turnover_rt: "0.15",
                    redeem_price: "110.000",
                    redeem_inc_cpn_fl: "y",
                    redeem_price_ratio: "130.000",
                    redeem_count_days: 15,
                    redeem_total_days: 30,
                    redeem_real_days: 0,
                    redeem_dt: null,
                    redeem_flag: "X",
                    orig_iss_amt: "15.000",
                    curr_iss_amt: "15.000",
                    rating_cd: "AAA",
                    issuer_rating_cd: "AAA",
                    guarantor: null,
                    ssc_dt: null,
                    esc_dt: null,
                    sc_notes: null,
                    market_cd: "szmb",
                    force_redeem: null,
                    real_force_redeem_price: null,
                    convert_cd: "未到转股期",
                    repo_cd: null,
                    ration: null,
                    ration_cd: null,
                    apply_cd: null,
                    online_offline_ratio: null,
                    qflag: "Q",
                    qflag2: "Q",
                    ration_rt: null,
                    fund_rt: "buy",
                    margin_flg: "R",
                    lt_bps: "",
                    pb: "1.50",
                    pb_flag: "N",
                    total_shares: "6129077211.0",
                    float_shares: "4938388153.0",
                    sqflg: "Y",
                    sprice: "8.27",
                    svolume: "133186.51",
                    sincrease_rt: "-1.19%",
                    qstatus: "00",
                    bond_value: "buy",
                    bond_value2: "buy",
                    volatility_rate: "buy",
                    last_time: "15:00:03",
                    convert_value: "161.21",
                    premium_rt: "-17.91%",
                    year_left: "3.756",
                    ytm_rt: "-3.94%",
                    ytm_rt_tax: "-4.58%",
                    price: "132.332",
                    full_price: "132.332",
                    increase_rt: "-2.12%",
                    volume: "297.16",
                    convert_price_valid: "Y",
                    adj_scnt: 0,
                    adj_cnt: 0,
                    redeem_icon: "",
                    ref_yield_info: "-",
                    adjust_tip: "",
                    adjusted: "N",
                    option_tip: "-",
                    bond_value3: "buy",
                    left_put_year: "-",
                    short_maturity_dt: "25-01-09",
                    dblow: "114.42",
                    force_redeem_price: "6.67",
                    put_convert_price: "3.59",
                    convert_amt_ratio: "3.7%",
                    convert_amt_ratio2: "3.0%",
                    convert_amt_ratio_tips: "转债占流动市值比：3.7% 转债占总市值比：3.0%",
                    stock_net_value: "0.00",
                    stock_cd: "000932",
                    pre_bond_id: "sz120004",
                    repo_valid: "有效期：2021-04-12 到 2021-04-12",
                    convert_cd_tip: "未到转股期；2021-08-26 开始转股",
                    price_tips: "全价：132.332 最后更新：15:00:03"
                }
            }
        }
        """
        def __init__(self, entries):
            # 债券代码
            self.bond_id = None
            # 债券名称
            self.bond_nm = None
            # 债券价格
            self.price = None
            # 债券价格全部。
            self.full_price = None
            # 涨跌幅
            self.increase_rt = None
            # 成交额
            self.volume = None

            # 正股代码
            self.stock_id = None
            # 正股名称
            self.stock_nm = None
            # 判断是可转债还是可交换债 E是可交换债 C是可转债
            self.btype = None
            # 转股价格
            self.convert_price = None
            # 交易开始期?， 即债券上市日期
            self.convert_price_valid_from = None
            # 转股开始日 债券发行日期
            self.convert_dt = None
            # 到期时间
            self.maturity_dt = None
            # 回售起始日
            self.next_put_dt = None
            #
            self.put_dt = None
            self.put_notes = None
            self.put_price = None
            self.put_inc_cpn_fl = None
            self.put_convert_price_ratio = None
            self.put_count_days = None
            self.put_total_days = None
            self.put_real_days = None
            self.repo_discount_rt = None
            self.repo_valid_from = None
            self.repo_valid_to = None
            # 当日换手率
            self.turnover_rt = None
            # 到期赎回价
            self.redeem_price = None
            self.redeem_inc_cpn_fl = None
            self.redeem_price_ratio = None
            self.redeem_count_days = None
            self.redeem_total_days = None
            self.redeem_real_days = None
            self.redeem_dt = None
            self.redeem_flag = None
            # 原始规模
            self.orig_iss_amt = None
            # 剩余规模
            self.curr_iss_amt = None
            # 评级
            self.rating_cd = None
            self.issuer_rating_cd = None
            # 是否担保
            self.guarantor = None
            self.ssc_dt = None
            self.esc_dt = None
            self.sc_notes = None
            self.market_cd = None
            self.force_redeem = None
            self.real_force_redeem_price = None
            self.convert_cd = None
            self.repo_cd = None
            self.ration = None
            # 配售代码
            self.ration_cd = None
            # 申购代码
            self.apply_cd = None
            #
            self.online_offline_ratio = None
            self.qflag = None
            self.qflag2 = None
            # 股东配售率
            self.ration_rt = None
            self.fund_rt = None
            self.margin_flg = None
            self.lt_bps = None
            # PB
            self.pb = None
            self.pb_flag = None
            # 总股份
            self.total_shares = None
            # 流通股份
            self.float_shares = None
            #
            self.sqflg = None
            # 正股价格
            self.sprice = None
            # 正股成交额
            self.svolume = None
            # 正股涨跌率
            self.sincrease_rt = None
            self.qstatus = None
            self.bond_value = None
            self.bond_value2 = None
            #
            self.volatility_rate = None
            # 数据更新最后时间
            self.last_time = None
            # 转股价值
            self.convert_value = None
            # 溢价率
            self.premium_rt = None
            # 剩余年限
            self.year_left = None
            # 到期收益率 税前
            self.ytm_rt = None
            # 到期收益率 税后
            self.ytm_rt_tax = None
            #
            self.convert_price_valid = None
            self.adj_scnt = None
            self.adj_cnt = None
            self.redeem_icon = None
            self.ref_yield_info = None
            self.adjust_tip = None
            self.adjusted = None
            self.option_tip = None
            self.bond_value3 = None
            #
            self.left_put_year = None
            # 到期时间
            self.short_maturity_dt = None
            # 双低价格
            self.dblow = None
            # 强赎价格
            self.force_redeem_price = None
            # 回售触发价
            self.put_convert_price = None
            # 转债占流动市值比
            self.convert_amt_ratio = None
            # 转债占总市值比
            self.convert_amt_ratio2 = None
            # 转债占流动市值比: 转债占总市值比
            self.convert_amt_ratio_tips = None
            #
            self.stock_net_value = None
            # 正股id
            self.stock_cd = None
            # 加前缀债券id sz sh
            self.pre_bond_id = None
            # 有效期
            self.repo_valid = None
            # 转股时间提示
            self.convert_cd_tip = None
            # 价格提示
            self.price_tips = None
            self.__dict__.update(entries)

    @staticmethod
    def __detect_active(info):
        """
        检测该债权是否上市交易
        :param info:
        :return:
        """
        c = info['convert_price_valid_from'] is None or info['price_tips'] == '待上市'
        if c:
            return False
        else:
            return True

    def __login(self):
        # 登录参数 涉及隐私 建议仓库改为私人仓
        params = {
            'return_url': 'https://www.jisilu.cn/',
            'user_name': '8550870a09c06319d9a0a5c677555a27',
            'password': '832ea9e7735118ea29b42c80b37a1146',
            'net_auto_login': '1',
            '_post_type': 'ajax',
            'aes': 1
        }
        address = 'https://www.jisilu.cn/account/ajax/login_process/'
        resp = requests.post(address, params)
        login_cookie = resp.headers['Set-Cookie']
        kbzw__Session = login_cookie[login_cookie.find('kbzw__Session=') + len('kbzw__Session=')
                                     :login_cookie.find(';', login_cookie.find('kbzw__Session='))]
        kbzw__user_login = login_cookie[login_cookie.rfind('kbzw__user_login=') + len('kbzw__user_login=')
                                     :login_cookie.find(';', login_cookie.rfind('kbzw__user_login='))]
        kbzw_r_uname = login_cookie[login_cookie.rfind('kbzw_r_uname=') + len('kbzw_r_uname=')
                                        :login_cookie.find(';', login_cookie.rfind('kbzw_r_uname='))]
        return {'kbzw__Session': kbzw__Session, 'kbzw__user_login': kbzw__user_login, 'kbzw_r_uname':kbzw_r_uname}

    def get_cookie(self):
        if self._cookie is None:
            self._cookie = self.__login()
        return self._cookie

    def update(self):
        cookie = self.get_cookie()
        timestamp = int(time.time() * 1000)
        jsl_address = 'https://www.jisilu.cn/data/cbnew/cb_list/?___jsl=LST___t={0}'.format(timestamp)
        response = requests.post(jsl_address, cookies=cookie)
        all_content = json.loads(response.text)
        self.page = all_content['page']
        self.total = all_content['total']
        self.bonds = []
        cbs, active_cbs = [], []
        for r in all_content['rows']:
            info = r['cell']
            bond = self.Bond(info)
            self.bonds.append(bond)
            cbs.append(info)
            if self.__detect_active(info):
                active_cbs.append(info)
        self._dict = all_content
        # 默认df 为活跃，all_df 包含未上市
        self.df = pd.DataFrame(active_cbs)
        self.all_df = pd.DataFrame(cbs)

    def __init__(self):
        self.page = None
        self.total = None
        self.bonds = None
        self._dict = None
        self.df = None
        self.all_df = None
        self._cookie = None
        # 获取最新数据
        self.update()

    def get_cb(self, cb_type='C'):
        """
        按种类划分可转债 和 可交换债
        :param cb_type:
        :return:
        """
        if cb_type == 'E' or cb_type == 'e':
            condition = self.df['btype'] == 'E'
        elif cb_type == 'C' or cb_type == 'c':
            condition = self.df['btype'] == 'C'
        else:
            condition = None
        return None if condition is None else pd.DataFrame(self.df[condition].copy())
