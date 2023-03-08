import yaml


class BasePage:
    # 存放公共变量
    def __init__(self):
        self.cookies = {
            "fat.auth.token": "FD3D61AA6AFF616519E04C3CF7AB87A0"
        }
        self.header = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        self.url = "https://faterp.szlcsc.com"
        self.order = "SO2303070251"

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



