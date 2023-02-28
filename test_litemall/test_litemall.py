import pytest
import requests


class TestLitemall:
    # 使用setup_class 提前完成变量申明
    def setup_class(self):
        url1 = "https://litemall.hogwarts.ceshiren.com/admin/auth/login"

        user_data = {
            "password": "test12345",
            "username": "hogwarts"
        }
        r = requests.post(url=url1, json=user_data)
        self.token = r.json()["data"]["token"]
        self.header = {"X-Litemall-Admin-Token": self.token}
        url2 = "https://litemall.hogwarts.ceshiren.com/wx/auth/login"
        client_data = {"username": "user123", "password": "user123"}
        r = requests.post(url2, json=client_data)
        self.client_token = r.json()["data"]["token"]

    def teardown(self):
        url = "https://litemall.hogwarts.ceshiren.com/admin/goods/delete"
        requests.post(url, json={"id": self.good_id}, headers=self.header)

    # 上架商品接口调试
    @pytest.mark.parametrize("goods_name", ["ADheysh12", "ADheysh13"])
    def test_add_goods(self, goods_name):

        url = "https://litemall.hogwarts.ceshiren.com/admin/goods/create"
        goods_data = {"goods": {"picUrl": "", "gallery": [], "isHot": False, "isNew": True, "isOnSale": True,
                                "goodsSn": "C256558", "name": goods_name, "counterPrice": "1.25"},
                      "specifications": [{"specification": "规格", "value": "标准", "picUrl": ""}],
                      "products": [{"id": 0, "specifications": ["标准"], "price": "10", "number": "10000", "url": ""}],
                      "attributes": []}
        # 问题：token是手动复制上去的
        # 解决：token需要自动获取并且赋值
        r = requests.post(url=url, headers=self.header, json=goods_data)
        print(r.json())
        goods_list_url = "https://litemall.hogwarts.ceshiren.com/admin/goods/list"
        goods_data = {
            "name": goods_name,
            "order": "desc",
            "sort": "add_time"
        }
        r = requests.get(goods_list_url, params=goods_data, headers=self.header)
        self.good_id = r.json()["data"]["list"][0]["id"]
        print(r.json())
        # =====获取商品详情接口
        goods_detail_url = "https://litemall.hogwarts.ceshiren.com/admin/goods/detail"
        r = requests.get(goods_detail_url, params={"id": self.good_id}, headers=self.header)
        product_id = r.json()["data"]['products'][0]["id"]
        # 加入购物车接口调试
        url = "https://litemall.hogwarts.ceshiren.com/wx/cart/add"
        # goodsId 、productId 需要自己增加
        cart_data = {"goodsId": self.good_id, "number": 1, "productId": product_id}
        r = requests.post(url, json=cart_data, headers={"X-Litemall-Token": self.client_token})
        res = r.json()
        assert res["errmsg"] == "成功"

