import jsonpath as jsonpath
import pymysql
import requests
import hamcrest
from hamcrest import assert_that, equal_to


class TestDemo:

    def test_get(self):
        r = requests.get("https://httpbin.testing-studio.com/get")
        print(r.status_code)
        print(r.json())
        print(r.text)
        assert r.status_code == 200

    def test_query(self):
        payload = {
            "level": 1,
            "name":"seveniruby"
        }
        r = requests.get("https://httpbin.testing-studio.com/get", params=payload)
        print(r.text)
        assert r.status_code == 200

    def test_post_form(self):
        payload = {
            "level": 1,
            "name": "seveniruby"
        }
        r = requests.post("https://httpbin.testing-studio.com/post", data=payload)
        print(r.text)
        assert r.status_code == 200

    def test_cookie(self):
        cookies = dict(cookies_are='working')
        r = requests.get("https://httpbin.testing-studio.com/cookies/set", cookies=cookies)
        assert r.status_code == 200

    # 访问立创erp 采购订单列表============================================================================================
    def test_cookie1(self):
        # 参数
        payload = {
            "purchaseTimeBegin": "2023-01-08 00:00: 00",
            "purchaseTimeEnd": "2023-02-07 23:59:59",
            "isOverseaBrokage": "false",
            "pageSize": 30,
            "currentPage": 1
        }
        # 传入token值
        cookies = {
            "fat.auth.token": "31357EB0EF711EF52FF703EEAE62E9E2"
        }
        r = requests.get("https://faterp.szlcsc.com/pms/purchase/order/page", cookies=cookies, params=payload)
        print(r.json())
        assert r.status_code == 200

    def test_file(self):
        files = {"file": open("reports.xls", 'rb')}
        r = requests.post("https://httpbin.testing-studio.com/post", files=files)
        assert r.status_code == 200

    #  Json请求体构造
    def test_post_json(self):
        payload = {
            "level": 1,
            "name": "seveniruby"
        }
        r = requests.post("https://httpbin.testing-studio.com/post", json=payload)
        print(r.text)
        assert r.status_code == 200
        assert r.json()['json']['level'] == 1

    # xml 请求构造

    # hancrest断言
    def test_hamcrest(self):
        r = requests.get("https://httpbin.testing-studio.com/categories.json")
        print(r.status_code)
        print(r.json())
        print(r.text)
        assert r.json()
        assert r.json()['headers']['Host'] == "httpbin.testing-studio.com"
        # assert_that(r.json()['categories_list']['categories'][0]['name'], equal_to("霍格沃兹学院公众号"))


    def test_headers(self):
        r = requests.get("https://httpbin.testing-studio.com/get", headers={"h": "header demo"})
        print(r.status_code)
        print(r.json())
        print(r.text)
        assert r.json()['headers']['H'] == 'header demo'
        assert r.json()['headers']['Host'] == "httpbin.testing-studio.com"

    # json 响应断言
    def test_hogwarts_json(self):
        r = requests.get("https://home.testing-studio.com/categories.json")
        print(r.text)
        assert r.status_code == 200
        # json  断言
        assert r.json()["category_list"]['categories'][0]['name'] == "提问区"

    # cookie 通过header传递
    def test_cookies(self):
        url = 'https://httpbin.testing-studio.com/cookies'
        header = {"Cookie": "hogwarts=school"}
        r = requests.get(url=url, headers=header)
        print(r.request.headers)

    # cookie 通过参数传递
    def test_cookies1(self):
        url = 'https://httpbin.testing-studio.com/cookies'
        header = {"User-Agent": "hogwarts"}
        cookie_data = {
            "hogwarts": "school",
            "teacher": "ad"
        }
        r = requests.get(url=url, headers=header, cookies=cookie_data)
        print(r.request.headers)

    # 通过form表单传入请求信息
    def test_data(self):
        data = {"hocwarts": "school"}
        r = requests.post("https://httpbin.testing-studio.com/post", data=data)
        print(r.json())

    # 通过json传入请求信息
    def test_json(self):
        data = {"hocwarts": "school"}
        r = requests.post("https://httpbin.testing-studio.com/post", json=data)
        print(r.json())

    # 超时处理
    def test_timeout(self):
        # timeout参数设置超时时间
        r = requests.get("https://httpbin.testing-studio.com/post", timeout=0.01)

    # 文件上传
    def test_files(self):
        files = {"file": open("reports.xls", 'rb')}
        r = requests.post("https://httpbin.testing-studio.com/post", files=files)
        assert r.status_code == 200

    # 操作数据库
    # 接口测试数据清理  delete 接口删除
    # 封装连接的数据库



















