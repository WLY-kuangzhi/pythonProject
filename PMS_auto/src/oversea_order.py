# 海外代购需求单
import requests

from PMS_auto.src.base_page import BasePage


class OverseaOrder(BasePage):
    def __init__(self):
        super(OverseaOrder, self).__init__()
        payload = {
            'orderCode': self.order,
            'currentPage': 1,
            'pageSize': 30
        }
        self.overseas_order = requests.get(url=self.url + '/pms/brokage/purchase/apply/page', cookies=self.cookies, params=payload)

    # 将需求单设置为手动带推单
    def handler_apply(self):
        data = []
        num = self.overseas_order.json()['result']['dataList']
        # 获取推单状态为 自动待推单 的需求单uuid
        for i in range(len(num)):
            if self.overseas_order.json()['result']['dataList'][i]['materialStatus'] == "auto_confirmed":
                data.append(len(self.overseas_order.json()['result']['dataList'][i]['uuid']))

            else:
                continue
        payload = {
            'uuidList': data
        }
        requests.post(url=self.url + '/pms/brokage/purchase/apply/handler', cookies=self.cookies, headers=self.header_x, params=payload)

    # 下推海外代购需求单
    def notify_delivery(self):
        num = self.overseas_order.json()['result']['dataList']
        for i in range(len(num)):
            payload = {
                'applyUuid': self.overseas_order.json()['result']['dataList'][i]['uuid'],
                'vendorUuid': self.overseas_order.json()['result']['dataList'][i]['vendorUuid'],
                'vendorName': self.overseas_order.json()['result']['dataList'][i]['vendorName'],
                'totalSendNum': self.overseas_order.json()['result']['dataList'][i]['canSendNumber'],
                'currencyType': self.overseas_order.json()['result']['dataList'][i]['currencyType'],
                'quotePrice': self.overseas_order.json()['result']['dataList'][i]['totalCostMoney']
            }
            requests.post(url=self.url + '/pms/brokage/purchase/apply/add/notify/delivery', cookies=self.cookies, headers=self.header_x, data=payload)












