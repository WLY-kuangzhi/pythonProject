from time import sleep

import yaml
import pytest

from test_PMS.src.base_page import BasePage
from test_PMS.src.high_price_stock_book import HighPriceStockBook
from test_PMS.src.jyb_quote import JybQuote
from test_PMS.src.notify import Notify
from test_PMS.src.purchase_order import PurchaseOrder
from test_PMS.src.sms_order import Order
from test_PMS.src.wait_notify import WaitNotify


# ===============销售订单采购流程自动化========================================
class TestJybQuote:
    def setup(self):
        self.order_data = {
            # 'productCode': 'C25351',
            "orderCode": 'SO2303010024',
            "currentPage": 1,
            "pageSize": 30
        }
        # 实例化列表
        self.quote = JybQuote(self.order_data)
        self.sms_order_auto = Order(self.order_data['orderCode'])
        self.high_price_stock_book = HighPriceStockBook(self.order_data['orderCode'])
        self.wait_notify = WaitNotify(self.order_data['orderCode'])
        self.notify = Notify(self.order_data['orderCode'])
        self.purchase_order = PurchaseOrder()

    # 交易部自动报价
    @pytest.mark.parametrize("quote_data", yaml.safe_load(open(r"../pms_data.yml", encoding='utf-8')))
    def test_jyb_auto_quote(self, quote_data):
        # 查询需求单
        aa = self.quote.get_query
        # 报价
        self.quote.save(quote_data)
        sleep(10)

    def test_get_quote_query(self):
        # 查询报价
        # self.quote.quote_query()
        # sleep(3)
        # 设置采购成本价
        self.quote.choose()

    def test_sms_auto(self):
        sleep(6)
        # 销售订单更新报价、允许支付
        self.sms_order_auto.order_book_detail()
        sleep(2)
        self.sms_order_auto.order_enable_price()
        sleep(2)
        self.sms_order_auto.order_allow_pay()

    # 采购流程
        # 待下推订货需求为空，存在两种情况
        # 1.在高价库存列表
        # 2.火箭消息未发送成功
    def test_pms_auto(self):
        high_price_book = self.high_price_stock_book.high_price_stock_book.json()['result']['dataList']
        wait_notify_none = self.wait_notify.get_wait_notify.json()['result']['dataList']
        if len(high_price_book) != 0:
            # 高价库存表确认订货
            self.high_price_stock_book.high_price_confirm()
            sleep(2)
            self.wait_notify.wait_notify()
        elif len(wait_notify_none) != 0:
            # 待下推订货需求
            self.wait_notify.wait_notify()
        else:
            print("没有查到需求单，火箭消息堵塞或者需求单已下推")
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










