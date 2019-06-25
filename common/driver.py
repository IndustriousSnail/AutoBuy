from selenium import webdriver


class Driver(object):

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--incognito")  # 隐身窗口
        options.add_argument("--headless")  # 隐藏窗口
        # options.add_argument("blink-settings=imagesEnabled=false")
        options.add_argument("--disable-gpu")
        self.driver = webdriver.Chrome(executable_path="./plugins/chromedriver75.exe", chrome_options=options)

    def get_driver(self):
        """获取webdriver对象"""
        return self.driver
