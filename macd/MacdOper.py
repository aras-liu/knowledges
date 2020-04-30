#!/usr/bin/python
# -*- coding: UTF-8 -*-

from ZApi import *
import Const
import logging
import sys
import os
import json
import smtplib
from email.mime.text import MIMEText
from cmnFuncs import *
from email.header import Header


class MacdOper:
    sender = 'lyk01024@163.com'
    receivers = ['1225548009@qq.com']
    zapi = ZApi(Const.ACC, Const.SEC)
    emacd = [[0.0, 0.0, 0.0, 0.0, 0.0]]
    max_dea = 0
    max_dif = 0

    time_scale = '1min'
    market = 'eth_qc'
    last_time = dict()
    last_buy_price = dict()
    mail_pass=''

    def send_mail_msg(self, title, msg):

        mail_host = "smtp.163.com"  # 设置服务器
        mail_user = "lyk01024@163.com"  # 用户名
        mail_pass = self.mail_pass

        message = MIMEText(msg, 'plain', 'utf-8')
        # message['From'] = Header("lyk01024", 'utf-8')  # 发送者
        # message['To'] = Header("1225548009@qq.com", 'utf-8')  # 接收者
        message['From'] = "lyk01024@163.com"  # 发送者
        message['To'] = "1225548009@qq.com"  # 接收者

        subject = title
        # message['Subject'] = Header(subject, 'utf-8')
        message['Subject'] = subject
        try:
            smtpObj = smtplib.SMTP_SSL("smtp.163.com", 465)
            # smtpObj = smtplib.SMTP()
            # smtpObj.set_debuglevel(1)
            # smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
            smtpObj.login(mail_user, mail_pass)
            smtpObj.sendmail(self.sender, self.receivers, message.as_string())
            print("邮件发送成功")
        except smtplib.SMTPException:
            print("Error: 无法发送邮件")

    def get_market_data(self):

        self.data = self.zapi.kline(self.market, self.time_scale)
        self.data = self.data.get('data')
        return True

    def init_config(self, tp=None):
        if tp is None:
            tp = 0
        if tp == 0:
            self.market = 'btc_qc'
            self.time_scale = '5min'
        elif tp == 1:
            self.market = 'eth_qc'
            self.time_scale = '5min'
        elif tp == 2:
            self.market = 'neo_qc'
            self.time_scale = '5min'
        else:
            self.market = 'btc_qc'
            self.time_scale = '5min'

        if self.mail_pass =='':
            self.mail_pass = input("请输入密码：")

    def main(self):
        self.init_config()
        # self.send_mail_msg("开始运行程序。。。", "测试邮件系统！")
        items =['btc_qc','eth_qc','ltc_qc','neo_qc','bsv_qc','qtum_qc']

        self.time_scale='5min'
        while True:
            for key in items:
                print(f"computing {key}")
                self.market=key
                try:
                    file_name = "price.json"
                    if os.path.exists(file_name):
                        file_data = read_file_txt(file_name)
                        self.last_buy_price = dict(json.loads(file_data))

                    self.real_time_macd()

                    save_txt(file_name,json.dumps(self.last_buy_price))
                except Exception as e:
                    print("这一轮出现异常，跳过")

                # file_name = "price.json"
                # if os.path.exists(file_name):
                #     file_data = read_file_txt(file_name)
                #     self.last_buy_price = dict(json.loads(file_data))
                #
                # self.real_time_macd()
                #
                # save_txt(file_name, json.dumps(self.last_buy_price))
            print(" 休息一下，等待下一轮！\n\n")

            time.sleep(30)

    def real_time_macd(self):
        """
            每隔一段时间获取一次 marker，判断最后两次的macd的值 是否出现叉
        """

        try:
            flag = self.get_market_data()
        except Exception as e:
            print("请求数据失败")
            flag = False
        self.judgement_of_zhixing()

        if not isinstance(self.data,list):
            print("请求数据失败，本轮跳过，可能存在超时")
            flag = False

        if flag:
            emacd = self.computeMACD()
            # last_emacd = [tm,ema12,ema26,dif,dea,bar,price],
            last_emacd = emacd[-1]

            last_time = last_emacd[0]
            last_key = f"{self.market}_{self.time_scale}"
            self.last_buy_price.setdefault(last_key,0)
            # 判断MACD 是否有更新
            if last_time == self.last_time.get(last_key):
                return False, 0

            self.last_time[last_key] = last_time
            fl, tp = self.check_curr_macd(emacd)
            print(f"cha flag={fl}, tp={tp}")
            if fl:
                self.judgement_of_cha(tp, last_emacd)
        return False, 0

    def judgement_of_zhixing(self):
        last_key = f"{self.market}_{self.time_scale}"
        last_price = self.last_buy_price.get(last_key)

        if last_price is None or last_price == 0:
            return
        last_price= float(last_price)
        cur_price = self.get_cur_price()
        rate_single = (cur_price - last_price) / cur_price
        if rate_single > 0.03:

            msg =f"如果金叉时购买，现在达到止盈价格，慎重卖出 {rate_single}"
            title =f"{self.market} 止盈卖出！！！"
            self.send_mail_msg(title,msg)
            print(f"注意！达到目标  {title} {msg}")
            self.last_buy_price.__setattr__(last_key, 0)
            return

    def judgement_of_cha(self, tp, last_emacd):
        last_key = f"{self.market}_{self.time_scale}"
        if tp == 0:
            # 金叉时 考虑进行购买
            msg = f"时间级别：{self.time_scale} ,币种 {self.market},出现 {'金叉' if tp == 0 else '死叉'}，参考连续情况进行判断买入。"
            self.send_mail_msg(f'买点判断 {self.market}',msg)
            print(f'\n 买点判断 {self.market} {msg}\n')
            self.last_buy_price[last_key]=last_emacd[-1]
        elif tp == 1:
            # 死叉时考虑卖出：1 出现死叉并且时下降趋势；2 出现死叉，收益虽没有达到总体目标，但是达到了死叉目标
            # 死叉暂时不买：1、出现死叉，但是收益没有跌破止损，或者收益很小。
            cur_price = last_emacd[-1]
            last_price = self.last_buy_price.get(last_key)
            if last_price is None or last_price == 0:
                self.send_mail_msg(f"卖点出现 {self.market}", f"出现死叉，系统中没有购买记录，慎重判断 {cur_price}")
                return
            last_price= float(last_price)
            rate_single = (cur_price - last_price) / cur_price
            sicha_zhiying = 0.005
            sicha_zhisun = -0.015
            if sicha_zhisun < rate_single and rate_single < sicha_zhiying:
                print(f"{rate_single} small shouyi ")
                return
            msg1 = f"如果在上个金叉，price={self.last_buy_price.get(last_key)},进行了购买，请参考。"

            if rate_single > 0:
                msg2 = f"止盈！止盈！\n 现在金额 {cur_price},出现死叉，并且收益[{rate_single}] 到达止盈，参考卖出。"
            else:
                msg2 = f"止损！止损！止损！\n 现在金额 {cur_price},出现死叉，并且收益[{rate_single}] 到达止损，参考卖出。"

            self.send_mail_msg(f"卖点出现 {self.market}",f"{msg1}\n{msg2}")
            print(f"\n---\n卖点出现{self.market} \n {msg1}\n{msg2}\n----\n")
            self.last_buy_price[last_key] =0
        else:
            return

    def check_curr_macd(self, emacd):

        dif1 = emacd[-2][3]
        dif2 = emacd[-1][3]

        dea1 = emacd[-2][4]
        dea2 = emacd[-1][4]

        rate = 0

        if dea1 > dif1 and dea2 < dif2:
            # 金叉
            if abs(dea1) > self.max_dif * rate:
                return True, 0
        elif dea1 < dif1 and dea2 > dif2:
            # 死叉
            if abs(dea1) > self.max_dif * rate:
                return True, 1
        else:
            return False, 0

        return False, 0

    def computeMACD(self):
        '''
            [
                [tm,ema12,ema26,dif,dea,bar,price],
                [],
            ]

        :return:
        '''
        emacd = [[0, 0, 0, 0, 0, 0, 0]]
        last_emacd = []
        for i in range(1, self.data.__len__()):
            item = self.data[i]
            tm = item[0]
            last_emacd = emacd[i - 1]
            ema12 = last_emacd[1] * (11 / 13.0) + float(item[4]) * (2 / 13.0)
            ema26 = last_emacd[2] * (25 / 27.0) + float(item[4]) * (2 / 27.0)
            dif = ema12 - ema26
            dea = last_emacd[4] * (8 / 10.0) + dif * (2 / 10.0)
            bar = 2 * (dif - dea)
            t = [tm, ema12, ema26, dif, dea, bar, item[4]]
            emacd.append(t)
            if self.max_dea < abs(dea):
                self.max_dea = abs(dea)
            if self.max_dif < abs(dif):
                self.max_dif = abs(dif)

        return emacd

        # print(f"self.max_dea={self.max_dea},self.max_dif={self.max_dif}")

    def run_macd(self):
        self.market = 'eth_qc'
        self.init_data()
        self.computeMACD()

        # 查找一个都为负并且  两条线相交  f=True  金叉
        # 查找一个都为正并且  两条线相交  f=False  死叉

        # f = True
        old = 0
        all_rate = 1
        print(f"self.emacd.__len__()={self.emacd.__len__()}")

        # for i in range(800, self.emacd.__len__()):
        tingdan_flag = False
        for i in range(200, 300):
            item = self.data[i]
            pr = float(float(item[2]) + float(item[3])) / 2
            if old != 0 and pr >= old * 1.03:
                rate_single = (pr - old) / pr
                print(f"达到目标  {rate_single}")
                all_rate = all_rate * (1 + rate_single) * (0.998)
                # all_rate = all_rate * (1 + rate_single)
                old = 0
                continue

            if old != 0 and pr < old * 0.99:
                rate_single = (pr - old) / pr
                print(f"止损  {rate_single}")
                # print(f"[{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(item[0] / 1000))}] curr price {item}")
                all_rate = all_rate * (1 + rate_single) * (0.998)
                # all_rate = all_rate * (1 + rate_single)
                tingdan_flag = True
                old = 0
                continue
            # print(f"[{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(item[0] / 1000))}] curr price {item}")
            # res = self.checkCha(f, i)
            (flag, tp) = self.checkcha2(i)
            # print(f"flag ={ flag},tp={tp}")
            if flag:
                rate_single = 0
                # print(f"出现 {'金叉叉' if tp == 0 else '死叉'}")
                # print(f"[{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(item[0] / 1000))}] curr price {item}")
                # print(f"\t{self.emacd[i - 1]}")
                # print(f"\t{self.emacd[i]}")
                if tp == 0 and old == 0:
                    # if tingdan_flag:
                    #     tingdan_flag = False
                    #     continue
                    old = pr
                else:
                    if old == 0:
                        continue
                    rate_single = (pr - old) / pr

                    if -0.015 < rate_single and rate_single < 0.005:
                        print(f"{rate_single} small shouyi ")
                        continue
                    print(f"单次 shou {rate_single}")
                    old = 0
                if rate_single != 0:
                    # all_rate = all_rate * (1 + rate_single)
                    all_rate = all_rate * (1 + rate_single) * (0.998)
        print(f"zong rate = {all_rate}")
        pass

    def get_cur_price(self):
        """
            获取实时买一价
        :return:
        """
        ticker = self.zapi.ticker(self.market).get('ticker')
        # print(ticker)
        # print(ticker.get('buy'))
        return float(ticker.get('buy'))


if __name__ == '__main__':
    mo = MacdOper()
    # mo.send_mail_msg("btc出现金叉", "jinshengoumai")
    mo.main()
