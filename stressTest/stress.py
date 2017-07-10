from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from parseCSV import get_user_list
import time
user_list = get_user_list()


for i in user_list:

    driver = webdriver.Chrome("./chromedriver")
    driver.get("http://ec2-52-23-166-162.compute-1.amazonaws.com/login")
    user_ID = driver.find_element_by_name('student_id')
    user_name = driver.find_element_by_name('last_name')
    survey_id = driver.find_element_by_name('survey_key')

    user_ID.send_keys(i[0])
    user_name.send_keys(i[1])
    survey_id.send_keys("T1")
    user_ID.submit()

