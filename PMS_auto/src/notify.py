# 通知单列表
import json
import requests
from PMS_auto.src.base_page import BasePage


class Notify(BasePage):
    def __init__(self):
        super(Notify, self).__init__()
        payload = {
            'orderCode': self.order,
            'pageSize': 30,
            'currentPage': 1
        }
        self.get_notify = requests.get(url=self.url + '/pms/notify/delivery/all/page', cookies=self.cookies, params=payload)

    # 通知单 审核通过
    def delivery_pass(self):
        num = len(self.get_notify.json()['result']['dataList'])
        for i in range(num):
            payload = {
                'uuidList': self.get_notify.json()['result']['dataList'][i]['uuid'],
                'isDoubleAudit': 'true'
            }
            requests.post(url=self.url + "/pms/notify/delivery/audit/pass", params=payload,
                            cookies=self.cookies)

    # PM审核
    def pm_pass(self):
        num = len(self.get_notify.json()['result']['dataList'])
        for i in range(num):
            payload = {
                'uuidList': self.get_notify.json()['result']['dataList'][i]['uuid'],
                'isDoubleAudit': 'true'
            }
            requests.post(url=self.url + "/pms/notify/delivery/audit/pmpass", params=payload,
                          cookies=self.cookies)

    # 经理审核
    def manager_pass(self):
        num = len(self.get_notify.json()['result']['dataList'])
        for i in range(num):
            payload = {
                'uuidList': self.get_notify.json()['result']['dataList'][i]['uuid'],
                'isDoubleAudit': 'true'
            }
            requests.post(url=self.url + "/pms/notify/delivery/manager/audit", params=payload,
                          cookies=self.cookies)

    # 大额审核
    def large_pass(self):
        num = len(self.get_notify.json()['result']['dataList'])
        for i in range(num):
            payload = {
                'uuidList': self.get_notify.json()['result']['dataList'][i]['uuid'],
                'isDoubleAudit': 'true'
            }
            requests.post(url=self.url + "/pms/notify/delivery/large/audit", params=payload,
                            cookies=self.cookies)

    # 下推国内采购订单
    def push_notify(self):
        num = len(self.get_notify.json()['result']['dataList'])
        for i in range(num):
            push_number = self.get_notify.json()['result']['dataList'][i]['needSendNumber']
            settle_org = self.get_notify.json()['result']['dataList'][i]['settleOrg']
            notify_uuid = self.get_notify.json()['result']['dataList'][i]['uuid']
            product_uuid = self.get_notify.json()['result']['dataList'][i]['productUuid']
            aa = {"avtTaxRate": 0.13, "serviceRate": 0.003, "currencyType": "rmb", "discountMoney": "0", "exchangeRate": 1,
              "expressName": "", "freightMoney": "0", "addFreightStatus": "wait", "otherMoney": "0", "prepayRate": 0,
              "remark": "", "settlementType": "owe", "specialMoney": "0", "accountName": "1714686311",
              "settleOrg": "js", "warehouseRecepitNo": "", "isAppendFee": False, "encrypt": False,
              "atmKey": "0da82c08c9f6d415ad1fe33fc5470609", "purchaseOrderDetails": [
                {"incidentalsMoney": "0", "isAllowPartAddstock": True,
                 "productUUID": product_uuid, "remark": "", "tariffRate": 0, "notifyDeliverys": [
                    {"pushNumber": push_number, "settleOrg": settle_org, "uuid": notify_uuid}],
                 "originPlace": ""}]}
            payload = json.dumps(aa)
            requests.post(url=self.url + "/pms/purchase/order/push", headers=self.header_j, data=payload,
                          cookies=self.cookies)




