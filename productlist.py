from selenium import webdriver
import time
import re
import pandas as pd
from pandas import DataFrame
from bs4 import BeautifulSoup
li=[]
driver = webdriver.Chrome(executable_path=r'C:\\driver\\chromedriver.exe')
#driver.get('https://www.amazon.in/s?k=soap')

def plist(lis):
	for j in lis:
		driver.get(j)
		soup = BeautifulSoup(driver.page_source, 'html.parser')
		images = soup.find_all("span", class_="a-size-base-plus a-color-base a-text-normal")
		for i in images:
			li.append(i.text)
		time.sleep(15)
	print(len(li))
	return li
lis=['https://www.amazon.in/s?k=soap','https://www.amazon.in/s?k=soap&page=2']
li=plist(lis)
print(li)

driver.close()
driver.quit()


#<span class="a-size-base-plus a-color-base a-text-normal" dir="auto">Dove Cream Beauty Bathing Bar, 100g (Pack of 3)</span>
#//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div[65]/span/div/div/ul/li[3]/a
