import time

import yaml


class BasePage:
    # 存放公共变量
    def __init__(self):
        self.cookies = {
            "fat.auth.token": "227D31CE7364F2A5AB62FB16B7A53B20"
        }
        self.header_x = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        self.url = "https://faterp.szlcsc.com"
        self.order = "SO2303100001"
        self.header_j = {"Content-Type": "application/json"}

    # 获取yaml文件内容
    def get_yaml_data(self):
        try:
            with open('../quote_data/quote_data.yml', encoding="utf-8") as f:
                data = yaml.load(f, Loader=yaml.FullLoader)
                return data
        except:
            return None

    # 修改yaml文件值
    def update_yaml_data(self, r, v):
        old_data = self.get_yaml_data()
        old_data[0][r] = v
        with open('../quote_data/quote_data.yml', "w", encoding="utf-8") as f:
            yaml.dump(old_data, f, allow_unicode=True)

    # 时间操作
    def C_time(self):
        today = time.localtime()
        day = 1
        tomorrow = time.strftime("%Y-%m-%d", time.localtime(time.time() + 86400 * day))
        today_time = today + '00: 00:00'
        tomorrow_time = tomorrow + '23:59:59'
        return today_time, tomorrow_time



