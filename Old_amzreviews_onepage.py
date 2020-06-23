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

#links='https://www.amazon.in/Lux-Touch-French-Almond-3x150/product-reviews/B00U1CAAJ8/'
#print(links)
di={}
column_names=['Id','Reviews','Date Reviewed','Ratings']
df = pd.DataFrame(columns = column_names)
driver = webdriver.Chrome(executable_path=r'C:\\driver\\chromedriver.exe')
links='https://www.amazon.in/Garnier-Anti-Pollution-Double-Action-Facewash/product-reviews/B07NQQPNDG'
driver.get(links)


def details(df):
	soup = BeautifulSoup(driver.page_source, 'html.parser')
	images = soup.find_all("div", class_=re.compile("a-section celwidget"))
	for i in images:
		if i.attrs['id'] != 'cm_cr-rvw_summary':
			#print('id    ',i.attrs['id'])
			di['Id']=i.attrs['id']
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
			
			#eprint('dict',di)
	return df
	# Looping in pages


def next(df):
	soup = BeautifulSoup(driver.page_source, 'html.parser')
	if soup.find("li", {"class": re.compile("^a-last$")}) is not None:
		print('inside if')
		df=details(df)
		print('shaping',df.shape,1)
		#print(df)
		time.sleep(10)

		element = driver.find_element_by_class_name("a-last")

		actions = ActionChains(driver)

		actions.move_to_element(element).perform()
		time.sleep(5)
		element.click()

		driver.execute_script("arguments[0].scrollIntoView();", element)

		next(df)

	else:
		print('error')
		df=details(df)
		driver.close()
		driver.quit()
		return df

df=next(df)

df.to_excel("output_reviews.xlsx")

#review id i.attrs['id'



	
