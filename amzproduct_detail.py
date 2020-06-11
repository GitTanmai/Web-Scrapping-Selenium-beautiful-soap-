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

options = Options()
di={}
column_names=['Product_Id','Product_Name','Price','Onshelfavalaiblity','Returnable','Sold_by','Rating','Delivered_by','Best_Before']
df = pd.DataFrame(columns = column_names)
#print('cols',df.columns)

links=['https://www.amazon.in/dp/B00HJ2E3Z0','https://www.amazon.in/dp/B082H9DFZ2','https://www.amazon.in/dp/B0744L529L','https://www.amazon.in/dp/B00B0QCNXU','https://www.amazon.in/dp/B07NQQPNDG','https://www.amazon.in/dp/B00X9UOCEI','https://www.amazon.in/dp/B006LX9VPU']
#print(links)
def details(links,df):
        for li in links:
                print('li',li)
                #options.add_argument("window-size=1200x600")
                driver = webdriver.Chrome(executable_path=r'C:\\driver\\chromedriver.exe')

                driver.get(li)
                time.sleep(5)

                di['Product_Id']=re.search(r'\/(?!.*\/).*',li).group(0)[1:]

                #Adding product name in dict
                pro = driver.find_element_by_xpath("//*[@id='productTitle']")
                di['Product_Name']=pro.text

                #Adding price to dict

                price_el=driver.find_element_by_xpath("//*[@id='priceblock_ourprice']")
                di['Price']=price_el.text

                #Adding availability in dict
                stock=driver.find_element_by_xpath("//*[@id='availability']/span")
                if stock.text=='In stock.':
                    di['Onshelfavalaiblity']=1
                else:
                    di['Onshelfavalaiblity']=0

                #Returnable
                try:
                        returna=driver.find_element_by_xpath("//*[@id='icon-farm-container']/div/div[2]/div[2]/span")
                        di['Returnable']=returna.text
                except:
                        returna=driver.find_element_by_xpath("//*[@id='icon-farm-container']/div/div[2]/span/div[2]/span")
                        di['Returnable']=returna.text  
                #Sold by 

                sold=driver.find_element_by_xpath("//*[@id='sellerProfileTriggerId']")
                di['Sold_by']=sold.text

                #Rating //*[@id="merchant-info"]/text()[2]
                
                time.sleep(15)
                try:
                        rating=driver.find_element_by_xpath("//*[@id='merchant-info']")
                        rat=re.search(r'\((.*?)\)',rating.text).group(1)
                except:
                        rat=None
                di['Rating']=rat

                #Delivery by
                try:
                        deliver=driver.find_element_by_xpath("//*[@id='ddmDeliveryMessage']/span")
                except:
                        deliver=driver.find_element_by_xpath("//*[@id='ddmDeliveryMessage']/b")
                #//*[@id="ddmDeliveryMessage"]/b 
                di['Delivered_by']=deliver.text

                #Best before 
                try:
                        bb=driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[4]/div[5]/div[4]/div[19]/span[2]")
                        bb=bb.text
                except:
                        bb=None
                di['Best_Before']=bb
                print('dict',di)
                df=df.append(di,ignore_index=True)
                
                #Closing the listening tool
                driver.close()
                driver.quit()
        return df
df=details(links,df)
df.index = np.arange(1, len(df) + 1)
df.to_excel("output.xlsx")
print(df)



