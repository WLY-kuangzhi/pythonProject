from time import sleep

import yaml
import pytest

from PMS_auto.src.base_page import BasePage
from PMS_auto.src.high_price_stock_book import HighPriceStockBook
from PMS_auto.src.jyb_quote import JybQuote
from PMS_auto.src.notify import Notify
from PMS_auto.src.purchase_order import PurchaseOrder
from PMS_auto.src.sms_order import Order
from PMS_auto.src.wait_notify import WaitNotify


# ===============销售订单采购流程自动化========================================
class TestJybQuote(BasePage):
    def setup(self):
        # 实例化列表
        self.quote = JybQuote()
        self.sms_order_auto = Order()
        self.high_price_stock_book = HighPriceStockBook()
        self.wait_notify = WaitNotify()
        self.notify = Notify()
        self.purchase_order = PurchaseOrder()

    # 交易部自动报价
    @pytest.mark.parametrize("quote_data", yaml.safe_load(open(r"../quote_data/quote_data.yml", encoding='utf-8')))
    def test_auto_quote(self, quote_data):
        # 报价
        sleep(5)
        self.quote.save(quote_data)
        sleep(10)
        # 设置采购成本价
        self.quote.choose()
        sleep(6)

    # 销售订单
    def test_sms_order(self):
        self.sms_order_auto.order_book_detail()
        sleep(3)
        self.sms_order_auto.order_enable_price()
        sleep(3)
        self.sms_order_auto.order_allow_pay()
        print('报价完成，请前往商城支付支付')

    # 采购流程
    def test_pms_auto(self):
        # 待下推订货需求为空，存在两种情况
        # 1.在高价库存列表
        # 2.火箭消息未发送成功
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
        product = self.sms_order_auto.order_detail()
        for i in range(len(product)):
            self.purchase_order.purchase_order_audit()
            self.purchase_order.purchase_manager_audit()
            self.purchase_order.purchase_large_audit()
        # 打印采购订单
            print(self.purchase_order.get_purchase_order(self.sms_order_auto.order_detail()))





