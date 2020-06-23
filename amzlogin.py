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
user='tm81739@gmail.com'
pwd='Tm@120894'
driver.get("https://www.amazon.in/")
try:
	id2=driver.find_element_by_xpath( '//*[@id="nav-signin-tooltip"]/a/span').click()
	time.sleep(10)
	
	# Opening page to enter mail id
	driver.find_element_by_xpath("//*[@id='ap_email']").send_keys(user)
	time.sleep(2)
	driver.find_element_by_xpath("//*[@id='continue']").click()
	
	#Opening page to enter password
	driver.find_element_by_xpath("//*[@id='ap_password']").send_keys(pwd)
	time.sleep(2)
	driver.find_element_by_xpath("//*[@id='signInSubmit']").click()
except:
	print('Error occurred while signing')
