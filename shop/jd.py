#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/16 20:50
# @Author  : zhaohf
# @Site    : 
# @File    : jd.py
# @Software: PyCharm
import datetime
import time

from selenium.webdriver import ActionChains

from common.driver import Driver
from common.model import Cookie
from crawler import jd_crawler
from log import log
from shop.base import Base
from utils import wait_utils, sqlite_utils
import threading


class JdThread(threading.Thread):

    def __init__(self, jd, price=None, in_stock=False, buy_time=None):
        super().__init__()
        self.jd = jd
        self.price = price
        self.in_stock = in_stock
        self.buy_time = buy_time
        self.is_stop = False
        self.success = None

    def run(self):
        sleep_time = 5.0  # 刷新间隔时间
        refresh_symbol = 0  # 刷新标记，每隔20s刷新一次，维持心跳
        while True:
            time.sleep(sleep_time)
            if self.is_stop:
                log.info("结束抢购线程")
                return
            goods_info = jd_crawler.get_goods_info_by_requests(self.jd.current_goods_id)  # http获取商品信息，接口，这个快
            if goods_info is None:
                log.error("获取商品信息失败")
                self.is_stop = True
                continue

            could_buy = True
            if self.price and float(goods_info.price) > float(self.price):
                # 如果给了价格条件，并且价格当前价格大于预期价格，先不买
                could_buy = False

            if self.in_stock and not goods_info.in_stock:
                could_buy = False

            # if self.buy_time and int(time.time()) < int(self.buy_time):
            #     could_buy = False

            if self.buy_time:
                remaining_time = self.buy_time - int(time.time())
                if remaining_time < 5:
                    sleep_time = 0.05
                elif remaining_time < 15:
                    sleep_time = 0.15
                elif remaining_time < 30:
                    sleep_time = 0.3
                else:
                    if refresh_symbol >= 4:
                        self.jd.driver.refresh()  # 刷新页面，维持心跳
                        refresh_symbol = 0
                    refresh_symbol += 1

            else:
                if refresh_symbol >= 4:
                    self.jd.driver.refresh()  # 刷新页面，维持心跳
                    refresh_symbol = 0
                refresh_symbol += 1

            if could_buy:
                log.info("达到购买条件，准备下单")
                if self.jd.order():
                    self.is_stop = True
                    self.success = True
                    log.info("下单成功")
                else:
                    self.is_stop = True
                    self.success = False
                    log.info("下单失败")
            else:
                log.info("不满足购买条件")
                log.info("商品价格：" + str(goods_info.price))
                log.info("是否有货:" + str(goods_info.in_stock))

    def stop(self):
        self.is_stop = True


class JD(Base):

    def __init__(self):
        self.jd_thread = None
        self.driver = None

    def init(self):
        driver = Driver().get_driver()
        driver.implicitly_wait(30)
        driver.maximize_window()
        self.driver = driver
        self.driver.get("http://www.jd.com")
        log.debug("打开京东页面")

    def open_login_page(self):
        wait_utils.open_page(self.driver, "https://passport.jd.com/new/login.aspx")

    def login(self, username, password):
        """
        账号密码方式登录京东
        todo 需要校验
        :param username:
        :param password:
        :return:
        """
        driver = self.driver
        self.open_login_page()

        login_tab = driver.find_element_by_link_text("账户登录")
        login_tab.click()

        login_name_text = driver.find_element_by_id("loginname")  # 账号
        login_name_text.clear()
        login_name_text.send_keys(username)
        log.debug("输入账号")

        login_password = driver.find_element_by_id("nloginpwd")  # 密码
        login_password.clear()
        login_password.send_keys(password)
        log.debug("输入密码")

        login_button = driver.find_element_by_link_text("登    录")
        login_button.click()
        log.debug("点击登陆按钮")

        login_verify = driver.find_element_by_id("JDJRV-wrap-loginsubmit")
        log.debug("需要人工验证")

    def login_qr(self):
        """
        扫码方式登陆
        :return:
        """
        driver = self.driver
        driver.get("https://www.jd.com")
        self.open_login_page()
        # 将滑块拖到最右边，然后再截屏
        driver.execute_script("window.scrollTo(10000,0)")
        # 截屏
        driver.save_screenshot("./qr_imgs/qr.png")
        # 打开图片
        # qr_utils.open_qr_img("qr.png")
        # log.info("请进行扫码登陆")
        # if wait_utils.until_url_contains(driver, "//www.jd.com"):
        #     log.info("用户登陆成功")
        # else:
        #     log.error("用户登陆超时")

    def open_goods_page(self, goods_url):
        self.driver.get(goods_url)
        if not wait_utils.until_url_contains(self.driver, "//item.jd.com/",
                                             retry_interval=0.01, timeout=5):
            log.error("打开商品页面失败")

    def get_user_name(self):
        wait_utils.open_page(self.driver, "https://www.jd.com")
        self.user_name = jd_crawler.get_user_name(self.driver.page_source)
        return self.user_name

    def open_address_page(self):
        self.driver.get("https://home.jd.com")  # 进入家目录
        user_setting = self.driver.find_elements_by_xpath('//*[@id="nav"]/div/div[3]/div[2]/div[1]')  # 账户设置
        ActionChains(self.driver).move_to_element(user_setting[0]).perform()  # 让鼠标悬浮在账户设置上
        # 找到收获地址按钮
        address_a = self.driver.find_elements_by_xpath('//*[@id="nav"]/div/div[3]/div[2]/div[2]/div/a[5]/span')
        address_a[0].click()
        if not wait_utils.until_url_contains(self.driver, "//easybuy.jd.com/address/getEasyBuyList.action",
                                             retry_interval=0.1, timeout=5):
            log.error("获取收获地址失败")

    def get_address(self):
        self.open_address_page()
        address_html = self.driver.page_source
        self.address_list = jd_crawler.get_address(address_html)
        return self.address_list

    def get_goods_info(self, goods_url):
        self.current_goods_url = goods_url
        if goods_url in self.driver.current_url:
            # 如果已经在这个商品页面上了，刷新该页面
            self.driver.refresh()
        else:
            # 如果不再这个商品页面，打开这个页面
            self.open_goods_page(goods_url)
        self.goods_info = jd_crawler.get_goods_info(self.driver.current_url, self.driver.page_source)
        self.current_goods_id = self.goods_info.id
        return self.goods_info

    def get_goods_info_from_cart(self):
        """从购物车获取商品详情"""
        start = datetime.datetime.now()
        wait_utils.open_page(self.driver, "https://cart.jd.com/cart.action", refresh=True)
        end = datetime.datetime.now()
        log.debug("刷新页面耗时：" + str((end - start).microseconds / 1000) + "毫秒")
        return jd_crawler.get_goods_info_from_cart(self.driver.page_source)

    def check_conditions_of_purchase(self, price=None):
        if self.goods_info.in_stock == '无货':
            return False

        if price:
            # 如果商品金额小于等于预期金额，则开始抢购
            if float(self.goods_info.price) <= price:
                return True
            else:
                return False

        return True

    def to_order_page(self):
        """进入订单页面"""
        wait_utils.open_page(self.driver, "https://cart.jd.com/cart.action")  # 打开购物车页面
        if "购物车空空的" in self.driver.page_source:
            # 购物车本来就是空的
            log.error("购物车为空")
            return

        self.driver.implicitly_wait(3)
        all_select_checkbox = self.driver.find_element_by_id("toggle-checkboxes_down")  # 点击全选按钮
        if all_select_checkbox.get_attribute("checked") == "true":
            pass
        else:
            all_select_checkbox.click()

        cart_submit_button = self.driver.find_element_by_link_text("去结算")
        cart_submit_button.click()
        if not wait_utils.until_url_contains(self.driver, "//trade.jd.com/shopping/order",
                                             retry_interval=0.01, timeout=60):
            log.error("打开订单页面异常")
            return False

    def order(self):
        # 找到提交订单按钮，并点击
        order_submit_button = self.driver.find_element_by_id("order-submit")
        order_submit_button.click()
        return True

    def save_cookies(self):
        cookies = self.driver.get_cookies()
        cookie_list = Cookie.from_dict(self.user_name, cookies)
        sqlite_utils.delete_cookies_by_username(self.user_name)
        # 将cookie存入数据库
        sqlite_utils.insert_cookies(cookie_list)

    def set_cookie(self, cookies):
        self.driver.delete_all_cookies()
        for item in cookies:
            self.driver.add_cookie(item.to_dict())

    def check_login_result(self):
        """检查登录结果"""
        wait_utils.open_page(self.driver, "https://www.jd.com/")
        return jd_crawler.check_login_result(self.driver.page_source)

    def start_rush_buy(self, price=None, in_stock=False, buy_time=None):
        """开始抢购"""
        if self.jd_thread and self.jd_thread.is_alive():
            # 已经在抢购了，需要先停止
            return False

        self.clear_cart()  # 清空购物车
        self.add_to_cart()  # 将商品加入购物车
        self.driver_to_no_image()  # 将driver转为无图片模式
        self.to_order_page()
        self.jd_thread = JdThread(self, price=price, in_stock=in_stock, buy_time=buy_time)
        self.jd_thread.start()  # 开始抢购
        return True

    def clear_cart(self):
        """清空购物车"""
        wait_utils.open_page(self.driver, "https://cart.jd.com/cart.action")  # 打开购物车页面
        if "购物车空空的" in self.driver.page_source:
            # 购物车本来就是空的
            return
        self.driver.implicitly_wait(3)
        log.debug("打开购物车页面")
        all_select_checkbox = self.driver.find_element_by_id("toggle-checkboxes_down")  # 点击全选按钮
        if all_select_checkbox.get_attribute("checked") == "true":
            pass
        else:
            all_select_checkbox.click()
        self.driver.implicitly_wait(3)
        self.driver.find_element_by_link_text("删除选中商品").click()  # 点击删除选中商品
        self.driver.implicitly_wait(3)
        self.driver.find_element_by_class_name("select-remove").click()  # 点击删除按钮
        log.info("清空购物车成功")
        time.sleep(2)  # 等待2s

    def add_to_cart(self):
        wait_utils.open_page(self.driver, self.current_goods_url)  # 打开商品页面
        log.debug("打开商品页面成功")
        self.driver.implicitly_wait(1)
        self.driver.find_element_by_link_text("加入购物车").click()  # 点击加入购物车
        log.info("加入购物车成功")
        wait_utils.until_url_contains(self.driver, "https://cart.jd.com/addToCart.html")

    def driver_to_no_image(self):
        """重新初始化driver，增加不加载图片属性，提高抢购效率"""
        self.driver.quit()  # 退出driver
        self.driver = Driver(imagesEnabled=False).get_driver()  # 重新获取driver
        self.driver.implicitly_wait(30)
        self.driver.get("http://www.jd.com")
        cookies = sqlite_utils.get_cookies_by_username(self.user_name)  # 从数据库中获取当前刚刚登录用户的cookies
        self.set_cookie(cookies)  # 将刚刚登录的用户的cookie重新设置进去
        self.driver.refresh()  # 刷新页面
