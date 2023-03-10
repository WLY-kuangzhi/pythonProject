import requests
import json

from PMS_auto.src.base_page import BasePage


class HighPriceStockBook(BasePage):
    def __init__(self):
        super(HighPriceStockBook, self).__init__()
        payload = {
            'orderCode': self.order,
            'confirmStatus': 'un_confirm',
            'currentPage': 1,
            'pageSize': 30
        }
        self.high_price_stock_book = requests.get(url=self.url + '/pms/high/price/stock/book/page', params=payload, cookies=self.cookies)

    def high_price_confirm(self):
        num = len(self.high_price_stock_book.json()['result']['dataList'])
        for i in range(num):

            high_price_uuid = self.high_price_stock_book.json()['result']['dataList'][i]['uuid']
            payload = {"uuidList": [high_price_uuid]}
            requests.post(url=self.url + '/pms/high/price/stock/book/confirm', data=json.dumps(payload),
                        cookies=self.cookies, headers=self.header_j)
