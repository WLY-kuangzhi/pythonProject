import requests

from test_PMS.src.base_page import BasePage


# 销售订单列表
class Order(BasePage):
    def __init__(self, order):
        super(Order, self).__init__()
    # 销售订单列表
        header = {
            "Content-Type": "application/json"
        }
        payload = {
            'isPayArles': False,
            'isWaitContactOrder': False,
            'customerAndOrderSplit': order,
            'scoreLevelList': None,
            'currentPage': 1,
            'pageSize': 30,
            'totalRow': 1,
            'operate': all
        }
        self.order = requests.get("https://faterp.szlcsc.com/sms/order/page", params=payload, cookies=self.cookies)

    # 询价详情
    def order_book_detail(self):
        payload = {
            'orderUuid': self.order.json()['result']['dataList'][0]['uuid']
        }
        r = requests.get("https://faterp.szlcsc.com/pms/order/bookorder/detail", params=payload, cookies=self.cookies)
        return r

    # 更新报价
    def order_enable_price(self):
        num = len(self.order_book_detail().json()['result'])
        i = 0
        for i in range(num):
            book_order_id = self.order_book_detail().json()['result'][i]['bookOrderId']
            payload = {
                'orderId': self.order.json()['result']['dataList'][0]['orderId'],
                'bookOrderId': book_order_id
            }
            r = requests.post("https://faterp.szlcsc.com/sms/order/enable/price", params=payload, cookies=self.cookies)
            i = i + 1

    # 允许支付
    def order_allow_pay(self):
        payload = {
            'uuid': self.order.json()['result']['dataList'][0]['uuid']
        }
        requests.post('https://faterp.szlcsc.com/sms/order/update/allow/pay', cookies=self.cookies, params=payload ,headers=self.header)
