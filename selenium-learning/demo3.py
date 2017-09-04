#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# drive.get打开url中的地址，webDriver将等待，直到页面全部加载完毕，然后返回执行你的脚本
driver = webdriver.Chrome(executable_path ='/Users/sugaryang/Desktop/chromedriver')

#打开python官网
driver.get("http://www.python.org")
assert "Python" in driver.title
#

elem = driver.find_element_by_name("q")

#开始输入关键字

# 清除输入框中的内容
elem.clear()
elem.send_keys("python")
#提交页面
elem.send_keys(Keys.RETURN)

#为了确定某些特定的结果被找到
assert "No result found" not in driver.page_source

# 关闭浏览器窗口
driver.close()

