#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/16 20:50
# @Author  : zhaohf
# @Site    : 
# @File    : jd.py
# @Software: PyCharm
import time

from selenium import webdriver

from common.driver import Driver
from log import log


class JD(object):

    def __init__(self):
        driver = Driver().get_driver()
        driver.implicitly_wait(30)
        driver.maximize_window()
        driver.get("http://www.jd.com")
        log.debug("打开京东页面")
        self.driver = driver

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


if __name__ == '__main__':
    jd = JD()
    jd.login_qr()
    time.sleep(10)
    jd.driver.quit()

