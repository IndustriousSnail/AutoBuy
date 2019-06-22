log_text = None
root = None


def gui_log(func):
    def wrapper(*args, **kwargs):
        log_text.config(state=tk.NORMAL)
        log_msg = func(*args, **kwargs)
        log_text.insert(tk.END, log_msg)
        log_text.config(state=tk.DISABLED)
        root.update()

    return wrapper


import time
import tkinter as tk
from threading import Thread
from tkinter import messagebox as msg


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
        self.root = tk.Tk()  # 创建窗口对象的背景色
        global root
        root = self.root
        self.root.geometry('800x500')
        self.root.resizable(0, 0)  # 阻止Python GUI的大小调整
        # self.login_init()  # 登录按钮初始化
        # self.shop_init(JD)  # 初始化商城页面, todo 选择抢购商城
        self.user_info_init()  # 初始化用户信息
        self.log_init()
        self.root.mainloop()  # 进入消息循环

    def login_init(self):
        login_frame = tk.Frame(self.root)
        login_button = tk.Button(login_frame, text='账号密码登录', width=20, height=2, command=self.login)
        login_button.pack(padx=50, pady=80)

        qr_login_button = tk.Button(login_frame, text='扫码登录', width=20, height=2, command=self.qr_login)
        qr_login_button.pack(padx=50)
        login_frame.pack(fill=tk.BOTH)
        self.login_frame = login_frame

    def shop_init(self, shop_class):
        self.shop_thread = Shop(shop_class)
        self.shop_thread.start()
        self.shop_instance = self.shop_thread.get_shop_instance()
        self.shop_thread.call(self.shop_instance.init)

    def login(self):
        msg.showwarning("提示", "暂不支持，敬请期待!")

    def qr_login(self):
        self.shop_thread.call(self.shop_instance.login_qr)

    def log_init(self):
        self.log_text = tk.Text(self.root, height=10, bg="white", fg="black")
        self.log_text.config(state=tk.DISABLED)
        self.log_text.pack(side=tk.BOTTOM, fill=tk.X)
        self.root.update()
        global log_text
        log_text = self.log_text

    def user_info_init(self):
        self.user_info_frame = tk.Frame(self.root)
        self.user_name = tk.StringVar(self.user_info_frame)
        self.user_name.set("唱跳Rap篮球")
        user_name_label = tk.Label(self.user_info_frame, textvar=self.user_name, fg='black', padx=10, pady=10)
        user_name_label.pack(side=tk.RIGHT)
        self.user_info_frame.pack(fill=tk.BOTH)

        self.address_list = tk.Listbox(self.user_info_frame, selectmode=tk.SINGLE)
        self.address_list.place(x=100, y=100, relwidth=0.9, relheight=0.9)

        for item in range(20):
            self.address_list.insert(tk.END, "练习时长两年半")
            self.address_list.insert(tk.END, "NBA形象大使")
            self.address_list.insert(tk.END, "踩徐坤")
        self.address_list.pack(side=tk.LEFT)

        yscrollbar = tk.Scrollbar(self.address_list, command=self.address_list.yview)
        yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.address_list.config(yscrollcommand=yscrollbar.set)
