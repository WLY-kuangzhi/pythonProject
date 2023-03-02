# 海外代购需求单
import requests

from test_PMS.src.base_page import BasePage


class OverseaOrder(BasePage):
    def __init__(self, oversea_order):
        super(OverseaOrder, self).__init__()
        payload = {
            'orderCode': oversea_order,
            'currentPage': 1,
            'pageSize': 30
        }
        self.overseas_order = requests.get('https://faterp.szlcsc.com/pms/brokage/purchase/apply/page', cookies=self.cookies, params=payload)

    # 将需求单设置为手动带推单
    def handler_apply(self):
        data = []
        num = self.overseas_order.json()['result']['dataList']
        i = 0
        # 获取推单状态为 自动待推单 的需求单uuid
        for i in range(len(num)):
            if self.overseas_order.json()['result']['dataList'][i]['materialStatus'] == "auto_confirmed":
                data.append(len(self.overseas_order.json()['result']['dataList'][i]['uuid']))

            else:
                continue
            i = i + 1
        payload = {
            'uuidList': data
        }
        requests.post('https://faterp.szlcsc.com/pms/brokage/purchase/apply/handler', cookies=self.cookies, headers=self.header, params=payload)

    # 下推海外代购需求单
    def notify_delivery(self):
        num = self.overseas_order.json()['result']['dataList']
        i = 0
        for i in range(len(num)):
            payload = {
                'applyUuid': self.overseas_order.json()['result']['dataList'][i]['uuid'],
                'vendorUuid': self.overseas_order.json()['result']['dataList'][i]['vendorUuid'],
                'vendorName': self.overseas_order.json()['result']['dataList'][i]['vendorName'],
                'totalSendNum': self.overseas_order.json()['result']['dataList'][i]['canSendNumber'],
                'currencyType': self.overseas_order.json()['result']['dataList'][i]['currencyType'],
                'quotePrice': self.overseas_order.json()['result']['dataList'][i]['totalCostMoney']
            }
            i = i + 1
            requests.post('https://faterp.szlcsc.com/pms/brokage/purchase/apply/add/notify/delivery', cookies=self.cookies, headers=self.header, data=payload)












