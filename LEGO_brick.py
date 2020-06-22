from selenium import webdriver
import time
import re
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options 
from pandas import DataFrame
import numpy as np
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains

driver = webdriver.Chrome(executable_path=r'C:\\driver\\chromedriver.exe')
links='https://brickset.com/sets/year-2016'
driver.get(links)
#lpage=driver.find_element_by_class_name("last")
#print(lpage.text)
def data():
	soup = BeautifulSoup(driver.page_source, 'html.parser')
	images = soup.find_all("div", class_="meta")
	#print('dsaaaaa       ',images[1].text)
	#quit()
	df_obj = pd.DataFrame(columns=['Pieces', 'Minifigs', 'RRP', 'PPP', 'Packaging', 'Availability', 'First sold', 'Additional images', 'Set type'])
	for i in images:
		print('LEGO id        ',i.find('span').text)
		print('LEGO name        ', re.search('(.*:)(.*)',i.find('h1').text).group(2).strip())
		dic={}
		vv=i.find_all('dd')
		kk=i.find_all('dt')
		for j,v in enumerate(kk):
			dic[kk[j].text]=vv[j].text
		df_obj = df_obj.append(dic, ignore_index=True)
	print(df_obj)
	driver.close()
	driver.quit()
	df_obj.to_excel("LEGO_output.xlsx")
data()
