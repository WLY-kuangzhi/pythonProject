# 交易部报价列表
import requests
from time import sleep
from PMS_auto.src.base_page import BasePage


class JybQuote(BasePage):
    # 查询需求单
    def __init__(self):
        # 可以使用父类的所有方法、变量等
        super(JybQuote, self).__init__()
        self.get_query = requests.post(url=self.url + "/pms/apply/star/page", params=self.order, headers=self.header_j, cookies=self.cookies)

    # 需求单报价
    def save(self, quote_data):
        num = len(self.get_query.json()['result']['dataList'])
        for i in range(num):
            # 获取需求单uuid、订单数量、商品uuid
            purchase_apply_uuid_list = self.get_query.json()['result']['dataList'][i]['uuid']
            order_number = self.get_query.json()['result']['dataList'][i]['orderNumber']
            product_uuid = self.get_query.json()['result']['dataList'][i]['productUuid']
            # 给yaml文件赋新值

            self.update_yaml_data("purchaseApplyUuidList", purchase_apply_uuid_list)
            self.update_yaml_data("orderNumber", order_number)
            self.update_yaml_data("productUuid", product_uuid)
            quote_data1 = self.get_yaml_data()[0]
            r = requests.post(url=self.url + "/pms/vendor/quote/star/save", params=quote_data1, headers=self.header_x, cookies=self.cookies)
            print(r.text)

    # 查询报价
    def quote_query(self):
        # 遍历返回结果，获取需求单报价的uuid ,加入到数组并返回
        num = len(self.get_query.json()['result']['dataList'])
        data = []
        for i in range(num):
            aa = {
                'purchaseApplyUuid': self.get_query.json()['result']['dataList'][i]['uuid']
            }
            r = requests.get(url=self.url + "/pms/vendor/quote/query", cookies=self.cookies, params=aa)
            vendor_quote_uuid = r.json()['result'][0]['uuid']
            data.append(vendor_quote_uuid)
        return data

    # 设置采购成本价
    def choose(self):
        data = self.quote_query()
        num = len(self.get_query.json()['result']['dataList'])
        i = 0
        for i in range(num):
            payload = {
                'uuid': self.get_query.json()['result']['dataList'][i]['uuid'],
                'vendorQuoteUuid': data[i]
            }
            r = requests.post(url=self.url + "/pms/apply/set/choose/cost/price", data=payload, cookies=self.cookies)
            print(r.json())
            sleep(2)

