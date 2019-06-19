import time
import tkinter as tk
from threading import Thread

from log import log
from tkinter import messagebox as msg

from shop.jd import JD
from utils import time_utils


class Shop(Thread):
    """该类进行Selenium操作，使用线程，不影响UI线程"""

    def __init__(self, shop_class):
        super().__init__()
        self.shop_class = shop_class
        # call上次被调用的事件，如果该事件该表，就重新调用call
        self.call_funcs = []
        self.shop = None

    def call(self, func, *args, **kwargs):
        self.call_funcs.append((func, args, kwargs))

    def get_shop_instance(self):
        """
        获取实例化后的商城实例
        :return:
        """
        while True:
            # run的第一步为初始化商城实例，当初始化完成后，返回实例
            if self.shop:
                return self.shop
            time.sleep(0.1)

    def run(self):
        self.shop = self.shop_class()  # 初始化商城类
        while True:
            if len(self.call_funcs) > 0:
                func, args, kwargs = self.call_funcs.pop(0)
                if args and kwargs:
                    func(args, kwargs)
                elif args:
                    func(args)
                elif kwargs:
                    func(kwargs)
                else:
                    func()
            # 每隔0.1s检测一次
            time.sleep(0.1)


class GUI(object):

    def __init__(self):
        root = tk.Tk()  # 创建窗口对象的背景色
        root.geometry('800x500')

        login_button = tk.Button(root, text='账号密码登录', width=20, height=2, command=self.login)
        login_button.pack(padx=50, pady=120)

        qr_login_button = tk.Button(root, text='扫码登录', width=20, height=2, command=self.qr_login)
        qr_login_button.pack(padx=50)

        self.shop_init(JD)  # 初始化商城页面, todo 选择抢购商城
        root.mainloop()  # 进入消息循环

    def shop_init(self, shop_class):
        self.shop_thread = Shop(shop_class)
        self.shop_thread.start()
        self.shop_instance = self.shop_thread.get_shop_instance()

    def login(self):
        msg.showwarning("提示", "暂不支持，敬请期待!")

    def qr_login(self):
        self.shop_thread.call(self.shop_instance.login_qr)


if __name__ == '__main__':
    GUI()
