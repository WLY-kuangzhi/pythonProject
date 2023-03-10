from time import sleep

from PMS_auto.src.notify import Notify
from PMS_auto.src.oversea_order import OverseaOrder
from PMS_auto.src.purchase_order import PurchaseOrder


class OverseaAuto:
    def setup(self):
        self.oversea_msg = {
            # 'productCode': 'C25351',
            "orderCode": 'SO2303010024',
            "currentPage": 1,
            "pageSize": 30
        }
        # 实例化列表
        self.oversea_order = OverseaOrder(self.oversea_msg['orderCode'])
        self.notify = Notify(self.oversea_msg['orderCode'])
        self.purchase_order = PurchaseOrder()

    def test_oversea_auto(self):
        self.oversea_order.handler_apply()
        self.oversea_order.notify_delivery()
        # 通知单
        sleep(5)
        self.notify.delivery_pass()
        self.notify.pm_pass()
        sleep(3)
        self.notify.manager_pass()
        sleep(3)
        self.notify.large_pass()
        # 海外代购需求单需下推香港采购订单


