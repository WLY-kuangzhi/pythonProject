# 交易部报价列表
from time import sleep

import requests

from test_PMS.src.base_page import BasePage


class JybQuote(BasePage):
    # 查询需求单
    def __init__(self, order_data):
        # 可以使用父类的所有方法、变量等
        super(JybQuote, self).__init__()
        header = {"Content-Type": "application/json"}
        self.get_query = requests.post("https://faterp.szlcsc.com/pms/apply/star/page", params=order_data, headers= header, cookies=self.cookies)

    # 需求单报价
    def save(self, quote_data):
        num = len(self.get_query.json()['result']['dataList'])
        i = 0
        for i in range(num):
            # 获取需求单uuid、订单数量
            purchase_apply_uuid_list = self.get_query.json()['result']['dataList'][i]['uuid']
            order_number = self.get_query.json()['result']['dataList'][i]['orderNumber']
            product_uuid = self.get_query.json()['result']['dataList'][i]['productUuid']
            # 给yaml文件赋新值
            self.update_yaml_data("purchaseApplyUuidList", purchase_apply_uuid_list)
            self.update_yaml_data("orderNumber", order_number)
            self.update_yaml_data("productUuid", product_uuid)
            r = requests.post("https://faterp.szlcsc.com/pms/vendor/quote/star/save", data=quote_data, headers=self.header,
                          cookies=self.cookies)
            sleep(3)
            print(r.text)
            i = i + 1

    # 查询报价
    def quote_query(self):
        # 遍历返回结果，获取需求单报价的uuid ,加入到数组并返回
        data = []
        for i in range(len(self.get_query.json()['result']['dataList'])):
            aa = {
                'purchaseApplyUuid': self.get_query.json()['result']['dataList'][i]['uuid']
            }
            r = requests.get("https://faterp.szlcsc.com/pms/vendor/quote/query", cookies=self.cookies, params=aa)
            data = data.append(r.json()['result'][0]['uuid'])
        return data

    # 设置采购成本价
    def choose(self):
        num = len(self.get_query.json()['result']['dataList'])
        i = 0
        for i in range(num):
            payload = {
                'uuid': self.get_query.json()['result']['dataList'][i]['uuid'],
                'vendorQuoteUuid': self.quote_query().data[i]
            }
            r = requests.post("https://faterp.szlcsc.com/pms/apply/set/choose/cost/price", params=payload, cookies=self.cookies)
            sleep(3)
            print(r.text)
