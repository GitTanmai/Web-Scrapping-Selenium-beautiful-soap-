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
import re



def data(df_obj):
	try:
		time.sleep(10)
		soup = BeautifulSoup(driver.page_source, 'html.parser')
		images = soup.find_all("div", class_="meta")
	except:
		df_obj.to_excel('LEGO.xlsx')
	#print(images)
	for i in images:
		dic={}
		dic['Id']=i.find('span').text
		dic['Name']=re.search('(.*:)(.*)',i.find('h1').text).group(2).strip()
		vv=i.find_all('dd')
		kk=i.find_all('dt')
		for j,v in enumerate(kk):
			dic[kk[j].text]=vv[j].text
		df_obj = df_obj.append(dic, ignore_index=True)
	return df_obj

if __name__ == '__main__':
	driver = webdriver.Chrome(executable_path=r'C:\\driver\\chromedriver.exe')
	links='https://brickset.com/sets/year-2016/page-1'
	driver.get(links)
	ssss=driver.find_elements_by_xpath('//*[@id="body"]/div[1]/div/div/div[1]/ul/li[13]/a')
	pages=int(re.search (r'(.*)-(\d+)',ssss[0].get_attribute("href")).group(2).strip())
	df_obj = pd.DataFrame(columns=['Name','Id','Pieces', 'Minifigs', 'RRP', 'PPP', 'Packaging', 'Availability', 'First sold', 'Additional images', 'Set type'])

	for i in range(1,pages+1):
		curpage=int(re.search (r'(.*)-(\d+)',links).group(2).strip())
		if i ==1:
			df_obj=data(df_obj)
			#print('if')
		else:
			link=re.search (r'(.*)-(\d+)',links).group(1).strip() +'-'+ str(i)
			#print('newlink',link)
			driver.get(link)
			#time.sleep(10)
			df_obj=data(df_obj)
	df_obj.to_excel('LEGO.xlsx')

	driver.close()
	driver.quit()

