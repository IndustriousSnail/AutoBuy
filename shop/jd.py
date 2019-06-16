#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/16 20:50
# @Author  : zhaohf
# @Site    : 
# @File    : jd.py
# @Software: PyCharm

from selenium import webdriver

if __name__ == '__main__':
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")

    driver = webdriver.Chrome(executable_path="../plugins/chromedriver.exe", chrome_options=options)
    driver.implicitly_wait(30)
    driver.maximize_window()  # 将窗口最大化

    driver.get("http://www.jd.com")

    login_link = driver.find_element_by_id("ttbar-login")  # 获取登录链接

    login_link.click()  # 点击登录按钮

    login_tab = driver.find_element_by_link_text("账户登录")
    login_tab.click()

    login_name_text = driver.find_element_by_id("loginname")  # 账号
    login_name_text.clear()
    login_name_text.send_keys("login_name")

    login_password = driver.find_element_by_id("nloginpwd")  # 密码
    login_password.clear()
    login_password.send_keys("password")

    login_button = driver.find_element_by_link_text("登    录")
    login_button.click()

