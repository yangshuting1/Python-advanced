#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

request_url=""

user_name=""
user_password=""


class youhujiaOrSearch(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(executable_path='/Users/sugaryang/Desktop/chromedriver')

    def test_search_in_login(self):
        driver = self.driver
        startTime = time.time()
        print "start time is: %0.3f" % startTime
        driver.set_page_load_timeout(40)
        driver.maximize_window()
        try:
            driver.get(request_url)
            # 隐形等待
            driver.implicitly_wait(30)
        except TimeoutException:
            print 'time out after 30 secodes when loading page'
            driver.execute_script('window.stop()')

        # 找到了手机号和密码的输入框
        login_phone = driver.find_element_by_name('phone')

        login_password = driver.find_element_by_name('password')

        login_phone.clear()
        login_password.clear()

        login_phone.send_keys(user_name)
        time.sleep(1)
        login_phone.send_keys(Keys.RETURN)

        login_password.send_keys(user_password)
        time.sleep(1)
        login_password.send_keys(Keys.RETURN)

        time.sleep(3)

        # 进入主页
        menu = driver.find_element_by_css_selector(".nav")

        # 一级:商品管理
        goods_manager_button = driver.find_element_by_css_selector('.nav .sideRoutes')
        ActionChains(driver).move_to_element(menu).click(goods_manager_button).perform()  # 链式用法
        # 商品管理-商品列表
        goods_list = driver.find_element_by_id('side-menu').find_element_by_class_name('nav')

        ActionChains(driver).move_to_element(menu).click(goods_list).perform()  # 链式用法
        time.sleep(2)

        # 找到状态框
        status = driver.find_element_by_xpath(
            "//*[@id='page-wrapper']/div/bw-goods-list/div[1]/div/div/div/form/div/div[2]/bw-chosen-plugins")

        ActionChains(driver).move_to_element(status).click(status).perform()  # 链式用法

        time.sleep(2)
        writing = driver.find_element_by_xpath(
            "//*[@id='page-wrapper']/div/bw-goods-list/div[1]/div/div/div/form/div/div[2]/bw-chosen-plugins/div/div/ul/li[2]")

        ActionChains(driver).move_to_element(status).click(writing).perform()  # 链式用法
        time.sleep(2)

        # 找到筛选按钮
        choose = driver.find_element_by_xpath("//*[@id='search']")

        # 鼠标移到此处
        ActionChains(driver).move_to_element(choose).click(choose).perform()  # 链式用法
        time.sleep(2)

        # 新建商品
        create_goods = driver.find_element_by_xpath(
            "//*[@id='page-wrapper']/div/bw-goods-list/div[1]/div/div/div/form/div/div[4]/button")

        ActionChains(driver).move_to_element(create_goods).click(create_goods).perform()

        time.sleep(2)

        good_name = driver.find_element_by_xpath("//*[@id='name']")

        good_time = driver.find_element_by_xpath("//*[@id='time']")

        good_name.clear()
        good_time.clear()

        good_name.send_keys("sss")
        time.sleep(1)
        good_name.send_keys(Keys.RETURN)

        time.sleep(5)

        # 一级: 资源管理
        source_manager = driver.find_element_by_xpath("//*[@id='side-menu']/li[3]/a/span[1]")

        # 主页
        main_page = driver.find_element_by_xpath("//*[@id='side-menu']/li[3]/ul/li[1]/a")

        ActionChains(driver).move_to_element(source_manager).click(source_manager).perform()

        time.sleep(3)

        ActionChains(driver).move_to_element(source_manager).click(main_page).perform()
        time.sleep(3)

        # 首页管理
        main_manager = driver.find_element_by_xpath("//*[@id='side-menu']/li[3]/ul/li[2]/a")

        ActionChains(driver).move_to_element(source_manager).click(main_manager).perform()

        time.sleep(5)

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
