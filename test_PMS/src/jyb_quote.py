# 交易部报价列表
import json
import time
from datetime import date, datetime

import requests

from test_PMS.src.base_page import BasePage


class JybQuote(BasePage):
    # 查询需求单
    def __init__(self, order_data):
        # 可以使用父类的所有方法、变量等
        super(JybQuote, self).__init__()
        header = {"Content-Type": "application/json"}
        self.get_query = requests.post("https://faterp.szlcsc.com/pms/apply/star/page", params=order_data, headers= header, cookies=self.cookies)
        self.num = len(self.get_query.json()['result']['dataList'])

    # 需求单报价
    def save(self, quote_data):
        i = 0
        for i in range(self.num):
            # 获取需求单uuid、订单数量
            purchase_apply_uuid_list = self.get_query.json()['result']['dataList'][i]['uuid']
            order_number = self.get_query.json()['result']['dataList'][i]['orderNumber']

            # 给yaml文件赋新值
            self.update_yaml_data("purchaseApplyUuidList", purchase_apply_uuid_list)
            self.update_yaml_data("orderNumber", order_number)

            i = i + 1

            requests.post("https://faterp.szlcsc.com/pms/vendor/quote/star/save", data=quote_data, headers=self.header,
                          cookies=self.cookies)

    # 查询报价
    def quote_query(self):
        aa = {
            'purchaseApplyUuid': self.get_query.json()['result']['dataList'][0]['uuid']
        }
        r = requests.get("https://faterp.szlcsc.com/pms/vendor/quote/query", cookies=self.cookies, params=aa)
        return r

    # 设置采购成本价
    def choose(self):
        i = 0
        for i in range(self.num):
            payload = {
                'uuid': self.get_query.json()['result']['dataList'][i]['uuid'],
                'vendorQuoteUuid': self.quote_query().json()['result'][i]['uuid']
            }
            requests.post("https://faterp.szlcsc.com/pms/apply/set/choose/cost/price", params=payload, cookies=self.cookies)
