from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options 
options = Options()

options.add_argument("window-size=1200x600")
driver = webdriver.Chrome(executable_path=r'C:\\driver\\chromedriver.exe')

driver.get("https://www.amazon.in/")
id2=driver.find_element_by_xpath( '//*[@id="nav-signin-tooltip"]/a/span').click()
time.sleep(10)

# Opening page to enter mail id
driver.find_element_by_xpath("//*[@id='ap_email']").send_keys('tm81739@gmail.com')
time.sleep(2)
driver.find_element_by_xpath("//*[@id='continue']").click()

#Opening page to enter password
driver.find_element_by_xpath("//*[@id='ap_password']").send_keys('Tm@120894')
time.sleep(2)
driver.find_element_by_xpath("//*[@id='signInSubmit']").click()
