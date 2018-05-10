from selenium import webdriver
from selenium.webdriver.common.by import By
import time
browser = webdriver.Chrome('C:\\Users\\NJ\Desktop\\test\\chromedriver.exe')
browser.get('https:/www.taobao.com')
input_first = browser.find_element(By.ID,'q')
input_first.send_keys('hello world')
time.sleep(5)
button = browser.find_element_by_class_name('btn-search')#找到搜索按钮
button.click()
time.sleep(5)
browser.close()