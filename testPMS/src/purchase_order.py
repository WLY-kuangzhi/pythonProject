# 采购订单列表
import requests

from testPMS.src.base_page import BasePage


class PurchaseOrder(BasePage):
    # 查询采购订单列表
    def __init__(self, product_code):
        super(PurchaseOrder, self).__init__()
        payload = {
            'productCode': product_code,
            'vendorName': 'G7962',
            'pageSize': 30,
            'currentPage': 1
        }
        self.get_purchase_order = requests.get(url=self.url + '/pms/purchase/order/page', cookies=self.cookies, params=payload)

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







