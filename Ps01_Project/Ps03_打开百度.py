from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# 设置webdriver
driver = webdriver.Chrome()

# 导航到百度网盘登录页面
driver.get("https://pan.baidu.com/")

# 查找并填写用户名字段
username = driver.find_element_by_id("TANGRAM__PSP_4__userName")

# 填写用户名
username.send_keys("19926558906")

# 查找并填写密码字段
password = driver.find_element_by_id("TANGRAM__PSP_4__password")

# 填写密码
password.send_keys("Pas$w0Rd@vip")

# 提交登录表单
password.send_keys(Keys.RETURN)

# 在网盘上继续所需的操作

# 等待10秒钟
time.sleep(10)

# 关闭webdriver
driver.close()
