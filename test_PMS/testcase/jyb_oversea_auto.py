from time import sleep

from test_PMS.src.notify import Notify
from test_PMS.src.oversea_order import OverseaOrder
from test_PMS.src.purchase_order import PurchaseOrder


class OverseaAuto:
    def setup(self):
        self.overseas_order_data = {
            # 'productCode': 'C25351',
            "orderCode": 'SO2303010024',
            "currentPage": 1,
            "pageSize": 30
        }
        # 实例化列表
        self.oversea_order = OverseaOrder(self.order_data['orderCode'])
        self.notify = Notify(self.order_data['orderCode'])
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
        sleep(3)
        self.notify.push_notify()
        sleep(5)
        # 采购订单
        self.purchase_order.purchase_order_audit()
        self.purchase_order.purchase_manager_audit()
        self.purchase_order.purchase_large_audit()
        print(self.purchase_order.get_purchase_order.json()['result']['dataList'][0]['purchaseOrderCode'])

