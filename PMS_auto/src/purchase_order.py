# 采购订单列表
import time

import requests

from PMS_auto.src.base_page import BasePage


class PurchaseOrder(BasePage):
    # 查询采购订单列表
    def __init__(self):
        super(PurchaseOrder, self).__init__()
        payload = {
            'vendorName': 'G7962',
            'purchaserName': '【测试】旷志1',
            'purchaseTimeBegin': self.C_time()['0'],
            'purchaseTimeEnd': self.C_time()['1'],
            'purchaseStatus': 'purchase',
            'auditStatus': 'wait_audit',
            'isOverseaBrokage': False,
            'pageSize': 30,
            'currentPage': 1
        }
        self.get_purchase_order = requests.get(url=self.url + '/pms/purchase/order/page', cookies=self.cookies, params=payload)

    # 打印采购订单
    def get_purchase_order(self):
            purchase_order_list = self.get_purchase_order.json()['result']['dataList'][0]['purchaseOrderCode']
            return purchase_order_list

    # 采购订单审核
    def purchase_order_audit(self):
        num = len(self.get_purchase_order.json()['result']['dataList'])
        for i in range(num):
            payload = {
                'uuid': self.get_purchase_order.json()['result']['dataList'][i]['uuid'],
                'isPass': 'true',
                'remark': '审核通过'
            }
            requests.post(url=self.url + "/pms/purchase/order/audit", params=payload,
                          cookies=self.cookies)

    # 采购订单经理审核
    def purchase_manager_audit(self):
        num = len(self.get_purchase_order.json()['result']['dataList'])
        for i in range(num):
            payload = {
                'uuid': self.get_purchase_order.json()['result']['dataList'][i]['uuid'],
                'isPass': 'true',
                'remark': '经理审核通过'
            }
            requests.post(url=self.url + "/pms/purchase/order/manager/audit", params=payload,
                        cookies=self.cookies)

    # 采购订单大额审核
    def purchase_large_audit(self):
        num = len(self.get_purchase_order.json()['result']['dataList'])
        for i in range(num):
            payload = {
                'uuid': self.get_purchase_order.json()['result']['dataList'][i]['uuid'],
                'isPass': 'true',
                'remark': '大额审核通过'
            }
            r = requests.post(url=self.url + "/pms/purchase/order/large/audit", params=payload,
                          cookies=self.cookies)
            assert r.status_code == 200







