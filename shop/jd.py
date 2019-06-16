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

    driver.get("http://www.baidu.com/")
