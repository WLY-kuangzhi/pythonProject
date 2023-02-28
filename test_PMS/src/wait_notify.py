# 待下推订货需求
import json

import requests

from test_PMS.src.base_page import BasePage


class WaitNotify(BasePage):
    # 查询
    def __init__(self, sms_order):
        super(WaitNotify, self).__init__()
        payload = {
            'isMine': False,
            'orderCode': sms_order,
            'pageSize': 30,
            'currentPage': 1
        }
        self.get_wait_notify = requests.get("https://faterp.szlcsc.com/pms/wait/notify/jyb/page", cookies=self.cookies, params=payload)

    # 待采购需求单下推通知单
    def wait_notify(self):
        header = {"content-type": "application/json"}
        num = len(self.get_wait_notify.json()['result']['dataList'])
        i = 0
        for i in range(num):
            wait_notify_uuid = self.get_wait_notify.json()['result']['dataList'][i]['uuid']
            wait_number = self.get_wait_notify.json()['result']['dataList'][i]['purchaseNumber']
            # 数据格式是json python 没有json格式，需要转换
            aa = [{
                "uuid": wait_notify_uuid,
                "notifyNumber": wait_number,
                "notifyRemark": "测试自动下推",
                "innerRemark": '测试自动下推'
            }]
            # 将元组转为json
            payload = json.dumps(aa)
            requests.post("https://faterp.szlcsc.com/pms/wait/notify/push/jyb", data=payload, headers=header,
                        cookies=self.cookies)
            i = i+1
