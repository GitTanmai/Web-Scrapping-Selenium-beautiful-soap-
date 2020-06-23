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


def details(df):
	di={}
	try:
		soup = BeautifulSoup(driver.page_source, 'html.parser')
		images = soup.find_all("div", class_=re.compile("a-section celwidget"))
		for i in images:
			try:
				if i.attrs['id'] != 'cm_cr-rvw_summary':
					#print('id    ',i.attrs['id'])
					di['Id']= re.search(r'(^customer_review-)(.*)',i.attrs['id']).group(2)
					desc=i.find('span',class_=re.compile("a-size-base review-text review-text-content"))
					#print('description',desc.text)
					di['Reviews']=desc.text.strip()
					dt=i.find('span',class_=re.compile("a-size-base a-color-secondary review-date"))
					#print('date',dt.text.split("on",1)[1] )
					di['Date Reviewed']=dt.text.split("on",1)[1] 
					rat=i.find('span',class_=re.compile("a-icon-alt"))
					#print('dtttttttttt',rat.text[:3])
					di['Ratings']=rat.text[:3]
					df=df.append(di,ignore_index=True)
			except:
				print('Error occur while fetching Summary ')
		
		if soup.find("li", {"class": re.compile("a-disabled a-last")}) is None:
			time.sleep(15)
			element = driver.find_element_by_class_name("a-last")
			actions = ActionChains(driver)
			actions.move_to_element(element).perform()
			time.sleep(5)
			element.click()
			driver.execute_script("arguments[0].scrollIntoView();", element)
			#print('ddas    ',df.shape)
			details(df)
		else:
			driver.close()
			driver.quit()
			df.drop_duplicates(inplace=True)
			df.to_excel(filename + '.xlsx')
			print(df.shape)
			return df
	except:
		print('Error while fetching reviews')
	# Looping in pages
if __name__ == '__main__':
	links=['https://www.amazon.in/Santoor-Sandal-Almond-Milk-Soap/product-reviews/B00B0QCNXU','https://www.amazon.in/Dove-Cream-Beauty-Bathing-100g/product-reviews/B0744L529L']
	try:
		driver = webdriver.Chrome(executable_path=r'C:\\driver\\chromedriver.exe')
	except:
		print('Driver unavailable')
	for lin in links:
		time.sleep(10)
		try:
			driver.get(lin)
			namecap=re.search(r'(^https:\/\/www.amazon.in\/)([A-Za-z0-9\.-]*)',lin).group(2)

			filename= 'Reviews ' + namecap + '.xlsx'
			column_names=['Id','Reviews','Date Reviewed','Ratings']
			df = pd.DataFrame(columns = column_names)
			print('filename    ',filename)
			print('df    ',df.shape)
			print('driver    ',driver)
		except:
			print('Error occured while fetching data')
