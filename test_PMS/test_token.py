# 交易部接口自动化流程
import json

import requests


class TestPMS:
    # 交易部报价--------------------------------------------------
    # 交易部列表查询
    def setup(self):
        self.cookies = {
            "fat.auth.token": "69F19FE3DFA02E856E486A41B37B3D73"
        }

    # 查询需求单
    def test_jyb_post(self):

        payload = {
            "productCode": "C14730",
            "orderCode": "WM2302080007",
            "currentPage": 1,
            "pageSize": 30
        }
        r = requests.post("https://faterp.szlcsc.com/pms/apply/star/page", params=payload, cookies=self.cookies)
        assert r.status_code == 200

    # 需求单报价
    def test_save(self):
        payload = {
            "achieveDateType": "in_stock",
            "arriveType": "book",
            "vendorUuid": "313B82C03522C1EC8E2F5D5A6D8617CD",
            "purchaserId": 11288,
            'purchaseApplyUuidList': 'FE76339DA9A5A859ABC2990F2645FA5C',
            'arriveDays': 10,
            'exchangeRate': 1,
            'toSaleExchangeRate': 1,
            'minOrderNum': 1,
            'priceWithTax': 0.3,
            'currencyType': 'rmb',
            'minPackNumber': 200,
            'validTime': '2023-02-22 00:00:00',
            'maxProvideNumber': -1,
            'minPackUnit': 'dai',
            'productArrange': 'daizhuang',
            'vendorName': 'G7962-国内-测试专用供应商（勿改）',
            'profitRate': 10,
            'isSpecificPrice': 'false',
            'productLastPrice': 0.33,
            'lastPriceCurrencyType': 'rmb',
            'productUuid': '705709BD470D44029C20BDE66104B1C5',
            'orderNumber': 50000,
            'salePrice': 0
        }
        r = requests.post("https://faterp.szlcsc.com/pms/vendor/quote/star/save", params=payload, cookies=self.cookies)
        assert r.status_code == 200

    # 查询报价
    def test_get_quote(self):
        # header = {'Accept-Encoding': 'gzip', 'Content-Type': 'application/json'}
        aa = {
            'purchaseApplyUuid': '922A8180B9AAC91EE19D9CDC65FDF08E'
        }
        r = requests.get("https://faterp.szlcsc.com/pms/vendor/quote/query", cookies=self.cookies, params=aa)
        quote_uuid = r.json()['result'][0]['uuid']
        print(quote_uuid)

    # 设置采购成本价
    def test_choose(self):
        payload = {
            'uuid':
                '75A84131A9D6763A34E0559C85AC84AB',
            'vendorQuoteUuid':
                'A10B0DE016E11364F4BA65AE78E95FC8'
        }
        requests.post("https://faterp.szlcsc.com/pms/apply/set/choose/cost/price", params=payload, cookies=self.cookies)

    # 销售订单列表
    def test_so(self):
        header = {
            "Content-Type": "application/json"
        }
        payload = {
            'isPayArles': False,
            'isWaitContactOrder': False,
            'customerAndOrderSplit': 'SO2302160007',
            'scoreLevelList': None,
            'currentPage': 1,
            'pageSize': 30,
            'totalRow': 1,
            'operate': all
        }
        r = requests.get("https://faterp.szlcsc.com/sms/order/page", params=payload, cookies=self.cookies)
        order_uuid = r.json()['result']['dataList'][0]['uuid']
        order_id = r.json()['result']['dataList'][0]['orderId']

        print(r.text)
        payload = {
            'orderCode': 'SO2302160007',
            'currentPage': 1,
            'pageSize': 30
        }
        r1 = requests.get('https://faterp.szlcsc.com/pms/high/price/stock/book/page',
                                                  params=payload, cookies=self.cookies)
        print(r1.json())

    # 询价详情
    def test_order_book_detail(self):
        payload = {
            'orderUuid': 'AC225460C611FB54F8B9A584F02387BD'
        }
        r = requests.get("https://faterp.szlcsc.com/pms/order/bookorder/detail", params=payload, cookies=self.cookies)
        book_order_id = r.json()['result'][0]['bookOrderId']

    # 更新报价
    def test_order_enable_price(self):
        payload = {
            'orderId': 34782512,
            'bookOrderId': 1346003
        }
        r = requests.post("https://faterp.szlcsc.com/sms/order/enable/price", params=payload, cookies=self.cookies)

    # 查询待下推订货需求
    def test_get_wait(self):
        pass

    def test_get_wait_notify(self):
        payload = {
            'isMine': False,
            'orderCode': 'SO2302130152',
            'pageSize': 30,
            'currentPage': 1
        }
        r = requests.get("https://faterp.szlcsc.com/pms/wait/notify/jyb/page", cookies=self.cookies, params=payload)
        print(r.json()['result']['dataList'][0]['uuid'])

    # 待采购需求单下推通知单
    def test_wait_notify(self):
        header = {"content-type": "application/json"}
        # 数据格式是json python 没有json格式，需要转换
        aa = [{"uuid": "17A098B02E37D60F20A76E83A8350B65", "notifyNumber": 5, "notifyRemark": None, "innerRemark": None}]
        # 将元组转为json
        payload = json.dumps(aa)
        r = requests.post("https://faterp.szlcsc.com/pms/wait/notify/push/jyb", payload, headers=header, cookies=self.cookies)
        assert r.status_code == 200
        print(r.text)

    # 通知单列表--------------------------------------------------
    # 通知单查询（全部）
    def test_get_notify(self):
        payload = {
            'orderCode': 'SO2302130152',
            'pageSize': 30,
            'currentPage': 1
        }
        r = requests.get('https://faterp.szlcsc.com/pms/notify/delivery/all/page', cookies=self.cookies, params=payload)
        print(r.json())

    # 通知单 审核通过
    def test_pass(self):
        payload = {
            'uuidList':'70B4E79E309EECCB05097624604BB95F',
            'isDoubleAudit': 'true'
        }
        r = requests.post("https://faterp.szlcsc.com/pms/notify/delivery/audit/pass", params=payload, cookies=self.cookies)
        assert r.status_code == 200

    # PM审核
    def test_pm_pass(self):
        payload = {
            'uuidList': '732CE9831771703BD3D61C34689274B8',
            'isDoubleAudit': 'true'
        }
        r = requests.post("https://faterp.szlcsc.com/pms/notify/delivery/audit/pmpass", params=payload, cookies=self.cookies)
        assert r.status_code == 200

    # 经理审核
    def test_manager_pass(self):
        payload = {
            'uuidList': '732CE9831771703BD3D61C34689274B8',
            # 'isDoubleAudit': 'true'
        }
        r = requests.post("https://faterp.szlcsc.com/pms/notify/delivery/manager/audit", params=payload, cookies=self.cookies)
        assert r.status_code == 200

    # 大额审核
    def test_large_pass(self):
        payload = {
            'uuidList': '732CE9831771703BD3D61C34689274B8',
            # 'isDoubleAudit': 'true'
        }
        r = requests.post("https://faterp.szlcsc.com/pms/notify/delivery/large/audit", params=payload, cookies=self.cookies)
        assert r.status_code == 200

    # 下推通知单
    def test_push_notify(self):
        header = {"content-type": "application/json"}
        aa = {"avtTaxRate": 0.13, "serviceRate": 0.003, "currencyType": "rmb", "discountMoney": "0",
                   "exchangeRate": 1, "expressName": "", "freightMoney": "0", "addFreightStatus": "wait",
                   "otherMoney": "0", "prepayRate": 0, "remark": "", "settlementType": "owe", "specialMoney": "0",
                   "accountName": "1714686311", "settleOrg": "zhlt", "warehouseRecepitNo": "", "isAppendFee": "false",
                   "encrypt": "false", "atmKey": "710467d708e1ba7e6d409045b381da79", "purchaseOrderDetails": [
                {"incidentalsMoney": "0", "isAllowPartAddstock": "true",
                 "productUUID": "1C77BDC9831A4F87B8C3B4A297027752", "remark": "", "tariffRate": 0, "notifyDeliverys": [
                    {"pushNumber": 1000, "settleOrg": "zhlt", "uuid": "BB1B0297B1632628118410A9F79717EC"}],
                 "originPlace": ""}]}
        payload = json.dumps(aa)
        r = requests.post("https://faterp.szlcsc.com/pms/purchase/order/push", headers=header, data=payload, cookies=self.cookies)
        print(r.text)
        assert r.status_code == 200

    # 采购订单列表
    def test_purchase_order(self):
        pass

    # 采购订单审核
    def test_purchase_order_audit(self):
        payload = {
            'uuid': '2969708CA32FF026205C08485005E3E8',
            'isPass': 'true',
            'remark': '审核通过'
        }
        r = requests.post("https://faterp.szlcsc.com/pms/notify/delivery/large/audit", params=payload,
                          cookies=self.cookies)
        assert r.status_code == 200

    # 采购订单经理审核
    # 采购订单大额审核





