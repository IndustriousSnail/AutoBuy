#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/16 20:50
# @Author  : zhaohf
# @Site    : 
# @File    : jd.py
# @Software: PyCharm
from selenium.webdriver import ActionChains

from common.driver import Driver
from common.model import Cookie
from crawler import jd_crawler
from log import log
from shop.base import Base
from utils import qr_utils, wait_utils, sqlite_utils


class JD(Base):

    def __init__(self):
        driver = Driver().get_driver()
        driver.implicitly_wait(30)
        driver.maximize_window()
        self.driver = driver

    def init(self):
        self.driver.get("http://www.jd.com")
        log.debug("打开京东页面")


    def open_login_page(self):
        driver = self.driver
        login_link = driver.find_element_by_id("ttbar-login")  # 获取登录链接

        login_link.click()  # 点击登录按钮
        log.debug("点击我要登陆链接")

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
        self.open_login_page()
        # 将滑块拖到最右边，然后再截屏
        driver.execute_script("window.scrollTo(10000,0)")
        # 截屏
        driver.save_screenshot("./qr_imgs/qr.png")
        # 打开图片
        qr_utils.open_qr_img("qr.png")
        log.info("请进行扫码登陆")
        if wait_utils.until_url_contains(driver, "//www.jd.com"):
            log.info("用户登陆成功")
        else:
            log.error("用户登陆超时")

    def open_goods_page(self, goods_url):
        self.driver.get(goods_url)
        if not wait_utils.until_url_contains(self.driver, "//item.jd.com/",
                                             retry_interval=0.1, timeout=5):
            log.error("打开商品页面失败")

    def get_user_name(self):
        user_name = jd_crawler.get_user_name(self.driver.page_source)
        return user_name

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
        self.open_goods_page(goods_url)
        self.goods_info = jd_crawler.get_goods_info(self.driver.current_url, self.driver.page_source)
        return self.goods_info

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

    def order(self):
        if self.goods_info.one_click_buy:
            # 有一键购按钮，默认当前页面是商品页面
            buy_button = self.driver.find_element_by_id("btn-onkeybuy")
            buy_button.click()
            if not wait_utils.until_url_contains(self.driver, "//trade.jd.com/shopping/order",
                                                 retry_interval=0.01, timeout=20):
                log.error("打开订单页面异常")
                return False
            # todo 进入订单页面

        # 下单失败
        return False

    def get_cookies(self):
        cookies = self.driver.get_cookies()
        cookie_list = Cookie.from_dict(cookies)
        # 将cookie存入数据库
        sqlite_utils.insert_cookies(cookie_list)

    def set_cookie(self, cookies):
        self.driver.delete_all_cookies()
        for item in cookies:
            print(item.to_dict())
            self.driver.add_cookie(item.to_dict())


